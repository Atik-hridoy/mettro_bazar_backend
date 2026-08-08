import uuid
from django.db import models
from django.conf import settings
from apps.products.models import Product, WeightVariant
from apps.delivery.models import DeliveryZone


class Cart(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True
    )
    session_id = models.CharField(max_length=100, blank=True, default='', db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f"Cart ({self.user or self.session_id})"


class CartItem(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(WeightVariant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_items'
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in cart"


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('SSLCOMMERZ', 'SSLCommerz'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('pending_collection', 'Pending Collection'),
    ]

    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    order_number = models.CharField(max_length=50, unique=True, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        null=True,
        blank=True
    )
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, db_index=True)
    delivery_address = models.TextField()
    delivery_zone = models.ForeignKey(
        DeliveryZone,
        on_delete=models.PROTECT,
        related_name='orders',
        null=True,
        blank=True
    )
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=8, decimal_places=2, default=60.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='COD')
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICES, default='pending')
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='pending', db_index=True)
    
    notes = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number} ({self.customer_name} - ৳{self.total_amount})"


class OrderItem(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    variant = models.ForeignKey(WeightVariant, on_delete=models.PROTECT, null=True, blank=True)
    
    product_name = models.CharField(max_length=255)
    variant_weight = models.CharField(max_length=50, blank=True, default='')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity}x {self.product_name} ({self.variant_weight})"
