from typing import Tuple, Dict, Any
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthService:
    @staticmethod
    def register_user(data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        phone = data['phone']
        password = data['password']
        name = data.get('name', '')
        address = data.get('address', '')

        if User.objects.filter(phone=phone).exists():
            return False, {"detail": "User with this phone number already exists."}

        user = User.objects.create_user(
            phone=phone,
            password=password,
            name=name,
            address=address
        )

        refresh = RefreshToken.for_user(user)

        return True, {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "phone": user.phone,
                "name": user.name or "Customer",
                "address": user.address or ""
            }
        }

    @staticmethod
    def login_user(phone: str, password: str) -> Tuple[bool, Dict[str, Any]]:
        user = authenticate(username=phone, password=password)
        if not user:
            # Fallback check if user exists by phone
            user = User.objects.filter(phone=phone).first()
            if not user or not user.check_password(password):
                return False, {"detail": "Invalid phone number or password."}

        if not user.is_active:
            return False, {"detail": "Account is disabled."}

        refresh = RefreshToken.for_user(user)

        return True, {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "phone": user.phone,
                "name": user.name or "Customer",
                "address": user.address or ""
            }
        }
