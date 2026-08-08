from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from apps.products.models import Category, Product, WeightVariant
from apps.orders.models import Order


class OrdersAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(id='cat-1', name='Meat', slug='meat')
        self.product = Product.objects.create(
            id='prod-1',
            name='Beef Curry',
            category=self.category,
            price=450.00
        )
        self.variant = WeightVariant.objects.create(
            id='v1-1',
            product=self.product,
            weight='500g',
            price=450.00,
            stock=50
        )

    def test_create_order(self):
        order_payload = {
            "customer_name": "Rahim Uddin",
            "phone": "01799887766",
            "delivery_address": "House 10, Road 5, Dhanmondi, Dhaka",
            "payment_method": "COD",
            "notes": "Call before delivery",
            "items": [
                {
                    "product_id": self.product.id,
                    "variant_id": self.variant.id,
                    "quantity": 2,
                    "unit_price": 450.00
                }
            ]
        }

        response = self.client.post('/api/orders/', order_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('orderNumber', response.data)
        self.assertEqual(response.data['payment_status'], 'pending_collection')
        self.assertEqual(response.data['payment_method'], 'COD')
        self.assertEqual(response.data['total_amount'], 960.0) # 450*2 + 60 delivery charge

        order_id = response.data['id']
        self.assertTrue(Order.objects.filter(id=order_id).exists())

    def test_get_order_by_id(self):
        order_payload = {
            "customer_name": "Karim",
            "phone": "01812345678",
            "delivery_address": "Gulshan 2, Dhaka",
            "items": [{"product_id": self.product.id, "quantity": 1, "unit_price": 450.00}]
        }
        create_res = self.client.post('/api/orders/', order_payload, format='json')
        order_id = create_res.data['id']

        response = self.client.get(f'/api/orders/{order_id}/?phone=01812345678')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], 'Karim')
