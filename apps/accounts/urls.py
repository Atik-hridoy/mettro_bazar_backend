from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, RegisterView, UserProfileView, UserAddressViewSet, AdminUserListView

router = DefaultRouter()
router.register(r'auth/addresses', UserAddressViewSet, basename='user_address')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/profile/', UserProfileView.as_view(), name='user_profile'),
    path('admin/customers/', AdminUserListView.as_view(), name='admin_customers'),
    path('', include(router.urls)),
]
