from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'variant', 'product_name', 'variant_weight', 'unit_price', 'quantity', 'total_price')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 
        'customer_name', 
        'phone', 
        'total_amount', 
        'payment_method', 
        'payment_status', 
        'order_status', 
        'created_at'
    )
    list_filter = ('order_status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'customer_name', 'phone')
    readonly_fields = ('order_number', 'subtotal', 'total_amount', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'created_at')
    search_fields = ('user__phone', 'session_id')
    inlines = [CartItemInline]
