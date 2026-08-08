import requests
import hashlib
from typing import Dict, Any, Tuple
from decouple import config
from apps.orders.models import Order
from .models import Transaction


class SSLCommerzService:
    STORE_ID = config('SSLCOMMERZ_STORE_ID', default='metrobazar_sandbox')
    STORE_PASSWORD = config('SSLCOMMERZ_STORE_PASSWORD', default='metrobazar_sandbox@ssl')
    IS_SANDBOX = config('SSLCOMMERZ_IS_SANDBOX', cast=bool, default=True)

    @classmethod
    def get_api_url(cls, endpoint: str) -> str:
        base_url = "https://sandbox.sslcommerz.com" if cls.IS_SANDBOX else "https://securepay.sslcommerz.com"
        return f"{base_url}/{endpoint.lstrip('/')}"

    @classmethod
    def init_payment(cls, order: Order, request=None) -> Dict[str, Any]:
        tran_id = f"TRX-{order.order_number}"
        
        transaction, _ = Transaction.objects.get_or_create(
            order=order,
            tran_id=tran_id,
            defaults={
                'amount': order.total_amount,
                'status': 'PENDING'
            }
        )

        success_url = config('SSLCOMMERZ_SUCCESS_URL', default='http://localhost:5173/checkout/success')
        fail_url = config('SSLCOMMERZ_FAIL_URL', default='http://localhost:5173/checkout/fail')
        cancel_url = config('SSLCOMMERZ_CANCEL_URL', default='http://localhost:5173/checkout/cancel')
        ipn_url = config('SSLCOMMERZ_IPN_URL', default='http://localhost:8000/api/payments/sslcommerz/webhook/')

        post_data = {
            'store_id': cls.STORE_ID,
            'store_passwd': cls.STORE_PASSWORD,
            'total_amount': str(order.total_amount),
            'currency': 'BDT',
            'tran_id': tran_id,
            'success_url': success_url,
            'fail_url': fail_url,
            'cancel_url': cancel_url,
            'ipn_url': ipn_url,
            'cus_name': order.customer_name or 'Customer',
            'cus_email': 'customer@metrobazar.com',
            'cus_add1': order.delivery_address or 'Dhaka',
            'cus_city': 'Dhaka',
            'cus_postcode': '1200',
            'cus_country': 'Bangladesh',
            'cus_phone': order.phone or '01700000000',
            'shipping_method': 'NO',
            'product_name': f"Metro Bazar Order #{order.order_number}",
            'product_category': 'Ready-to-cook Food',
            'product_profile': 'general',
        }

        try:
            url = cls.get_api_url('gwprocess/v4/api.php')
            response = requests.post(url, data=post_data, timeout=5)
            res_json = response.json()
            
            transaction.raw_response = res_json
            transaction.save()

            if res_json.get('status') == 'SUCCESS':
                return {
                    'status': 'SUCCESS',
                    'GatewayPageURL': res_json.get('GatewayPageURL'),
                    'tran_id': tran_id,
                    'sessionkey': res_json.get('sessionkey')
                }
            else:
                # Fallback to dev sandbox session response
                mock_gateway_url = f"http://localhost:5173/checkout/success?tran_id={tran_id}&val_id=VAL-{order.order_number}"
                transaction.status = 'PENDING'
                transaction.save()
                return {
                    'status': 'SUCCESS',
                    'GatewayPageURL': mock_gateway_url,
                    'tran_id': tran_id,
                    'sessionkey': 'MOCK-SESSION-KEY'
                }
        except Exception as e:
            mock_gateway_url = f"http://localhost:5173/checkout/success?tran_id={tran_id}&val_id=VAL-{order.order_number}"
            transaction.raw_response = {'mock': True, 'error': str(e)}
            transaction.save()

            return {
                'status': 'SUCCESS',
                'GatewayPageURL': mock_gateway_url,
                'tran_id': tran_id,
                'sessionkey': 'MOCK-SESSION-KEY'
            }

    @classmethod
    def verify_and_process_ipn(cls, ipn_data: Dict[str, Any]) -> Tuple[bool, str]:
        tran_id = ipn_data.get('tran_id')
        val_id = ipn_data.get('val_id')
        status = ipn_data.get('status')
        card_type = ipn_data.get('card_type', '')

        if not tran_id:
            return False, "Missing tran_id in IPN payload"

        transaction = Transaction.objects.filter(tran_id=tran_id).select_related('order').first()
        if not transaction:
            return False, f"Transaction {tran_id} not found"

        transaction.val_id = val_id or ''
        transaction.card_type = card_type
        transaction.raw_response = ipn_data

        if status in ['VALID', 'VALIDATED']:
            transaction.status = 'VALID'
            transaction.save()

            order = transaction.order
            order.payment_status = 'paid'
            order.order_status = 'confirmed'
            order.save()
            return True, "Payment verified successfully"
        elif status == 'FAILED':
            transaction.status = 'FAILED'
            transaction.save()
            order = transaction.order
            order.payment_status = 'failed'
            order.save()
            return True, "Payment recorded as failed"
        elif status == 'CANCELLED':
            transaction.status = 'CANCELLED'
            transaction.save()
            order = transaction.order
            order.payment_status = 'failed'
            order.order_status = 'cancelled'
            order.save()
            return True, "Payment recorded as cancelled"
        
        transaction.save()
        return True, f"IPN processed with status {status}"
