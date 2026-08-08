from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserAddress, OTPDevice


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('phone', 'name', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('phone', 'name')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name', 'address', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('phone', 'name', 'password', 'is_staff', 'is_active'),
            },
        ),
    )


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('label', 'user', 'full_name', 'phone', 'city', 'is_default', 'created_at')
    list_filter = ('city', 'is_default')
    search_fields = ('user__phone', 'full_name', 'address', 'label')


@admin.register(OTPDevice)
class OTPDeviceAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'is_verified', 'expires_at', 'created_at')
    list_filter = ('is_verified',)
    search_fields = ('phone', 'code')
    readonly_fields = ('created_at', 'updated_at')
