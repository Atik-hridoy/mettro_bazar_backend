import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone number must be set')
        phone = phone.strip()
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=255, blank=True, default='')
    address = models.TextField(blank=True, default='')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.phone} ({self.name or 'No Name'})"


class UserAddress(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_addresses')
    label = models.CharField(max_length=50, help_text="e.g. Home, Work, Office")
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=100, default='Dhaka')
    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_addresses'
        verbose_name = 'User Address'
        verbose_name_plural = 'User Addresses'
        ordering = ['-is_default', '-created_at']

    def save(self, *args, **kwargs):
        if self.is_default:
            UserAddress.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label} - {self.full_name} ({self.address})"


class OTPDevice(models.Model):
    phone = models.CharField(max_length=20, db_index=True)
    code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'otp_devices'
        verbose_name = 'OTP Device'
        verbose_name_plural = 'OTP Devices'
        ordering = ['-created_at']

    def is_valid(self) -> bool:
        return not self.is_verified and timezone.now() < self.expires_at

    def __str__(self):
        return f"OTP for {self.phone}: {self.code}"
