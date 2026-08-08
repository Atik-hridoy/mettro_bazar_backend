from django.urls import path
from .views import SSLCommerzInitView, SSLCommerzWebhookView

urlpatterns = [
    path('payments/sslcommerz/init/', SSLCommerzInitView.as_view(), name='sslcommerz_init'),
    path('payments/sslcommerz/webhook/', SSLCommerzWebhookView.as_view(), name='sslcommerz_webhook'),
]
