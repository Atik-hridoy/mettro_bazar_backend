from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from apps.products.models import Category, Product
from apps.orders.models import Order
from apps.payments.models import Transaction


class PaymentsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(id='cat-1', name='Meat', slug='meat')
        self.product = Product.objects.create(id='p1', name='Chicken', category=self.category, price=300)
        self.order = Order.objects.create(
            order_number='MB-TEST01',
            customer_name='Test User',
            phone='01700000000',
            delivery_address='Banani',
            subtotal=300,
            delivery_charge=60,
            total_amount=360,
            payment_method='SSLCOMMERZ',
            payment_status='pending'
        )

    def test_sslcommerz_init_payment(self):
        response = self.client.post('/api/payments/sslcommerz/init/', {'order_id': self.order.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertIn('GatewayPageURL', response.data)
        self.assertTrue(Transaction.objects.filter(order=self.order).exists())

    def test_sslcommerz_ipn_webhook(self):
        # Init payment first
        init_res = self.client.post('/api/payments/sslcommerz/init/', {'order_id': self.order.id}, format='json')
        tran_id = init_res.data['tran_id']

        ipn_payload = {
            'tran_id': tran_id,
            'val_id': 'VAL-12345',
            'status': 'VALID',
            'card_type': 'VISA-DBBL'
        }

        response = self.client.post('/api/payments/sslcommerz/webhook/', ipn_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.order.refresh_from_db()
        self.assertEqual(self.order.payment_status, 'paid')
        self.assertEqual(self.order.order_status, 'confirmed')

        trx = Transaction.objects.get(tran_id=tran_id)
        self.assertEqual(trx.status, 'VALID')
        self.assertEqual(trx.val_id, 'VAL-12345')
