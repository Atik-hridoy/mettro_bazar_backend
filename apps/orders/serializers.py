from rest_framework import serializers
from apps.products.models import Product, WeightVariant
from apps.products.serializers import ProductListSerializer, WeightVariantSerializer
from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    selectedVariant = WeightVariantSerializer(source='variant', read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    variant_id = serializers.PrimaryKeyRelatedField(
        queryset=WeightVariant.objects.all(), source='variant', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'selectedVariant', 'product_id', 'variant_id', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    unitPrice = serializers.FloatField(source='unit_price', read_only=True)
    totalPrice = serializers.FloatField(source='total_price', read_only=True)
    productName = serializers.CharField(source='product_name', read_only=True)
    variantWeight = serializers.CharField(source='variant_weight', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 
            'product', 
            'variant', 
            'productName', 
            'product_name', 
            'variantWeight', 
            'variant_weight', 
            'unitPrice', 
            'unit_price', 
            'quantity', 
            'totalPrice', 
            'total_price'
        ]


class OrderListSerializer(serializers.ModelSerializer):
    customerName = serializers.CharField(source='customer_name', read_only=True)
    orderNumber = serializers.CharField(source='order_number', read_only=True)
    deliveryAddress = serializers.CharField(source='delivery_address', read_only=True)
    deliveryCharge = serializers.FloatField(source='delivery_charge', read_only=True)
    subtotal = serializers.FloatField(read_only=True)
    totalAmount = serializers.FloatField(source='total_amount', read_only=True)
    paymentMethod = serializers.CharField(source='payment_method', read_only=True)
    paymentStatus = serializers.CharField(source='payment_status', read_only=True)
    orderStatus = serializers.CharField(source='order_status', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'orderNumber',
            'order_number',
            'customerName',
            'customer_name',
            'phone',
            'deliveryAddress',
            'delivery_address',
            'subtotal',
            'deliveryCharge',
            'delivery_charge',
            'totalAmount',
            'total_amount',
            'paymentMethod',
            'payment_method',
            'paymentStatus',
            'payment_status',
            'orderStatus',
            'order_status',
            'created_at'
        ]


class OrderDetailSerializer(OrderListSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta(OrderListSerializer.Meta):
        fields = OrderListSerializer.Meta.fields + ['items', 'notes']


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.CharField(required=True)
    variant_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    quantity = serializers.IntegerField(min_value=1, default=1)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=255, required=True)
    phone = serializers.CharField(max_length=20, required=True)
    delivery_address = serializers.CharField(required=True)
    delivery_zone_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    payment_method = serializers.ChoiceField(choices=['COD', 'SSLCOMMERZ'], default='COD')
    notes = serializers.CharField(required=False, allow_blank=True, default='')
    items = OrderItemInputSerializer(many=True, required=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value
