from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserAddress

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=128, required=True)

    def validate_phone(self, value):
        return value.strip()


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=128, min_length=4, required=True)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')
    address = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_phone(self, value):
        value = value.strip()
        if not value or len(value) < 4:
            raise serializers.ValidationError("Please enter a valid phone number or username")
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("An account with this phone number already exists.")
        return value


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    isAdmin = serializers.BooleanField(source='is_staff', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone', 'name', 'address', 'avatar', 'avatar_url', 'isAdmin', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_avatar_url(self, obj) -> str:
        request = self.context.get('request')
        if obj.avatar:
            if request is not None:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return ''


class UserAddressSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source='full_name')
    isDefault = serializers.BooleanField(source='is_default', default=False)

    class Meta:
        model = UserAddress
        fields = ['id', 'label', 'fullName', 'full_name', 'phone', 'address', 'city', 'isDefault', 'is_default', 'created_at']
        read_only_fields = ['id', 'created_at']
