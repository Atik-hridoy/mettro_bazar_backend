from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, CartSyncView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('cart/', CartSyncView.as_view(), name='cart_sync'),
    path('', include(router.urls)),
]
