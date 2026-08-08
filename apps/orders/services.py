import random
import string
from decimal import Decimal
from typing import Dict, Any
from django.db import transaction
from apps.products.models import Product, WeightVariant
from apps.delivery.models import DeliveryZone
from .models import Order, OrderItem


class OrderService:
    @staticmethod
    def generate_order_number() -> str:
        """Generates unique order number format MB-XXXXXX"""
        while True:
            digits = ''.join(random.choices(string.digits, k=6))
            order_number = f"MB-{digits}"
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number

    @classmethod
    @transaction.atomic
    def create_order(cls, user, data: Dict[str, Any]) -> Order:
        customer_name = data['customer_name']
        phone = data['phone']
        delivery_address = data['delivery_address']
        payment_method = data.get('payment_method', 'COD')
        notes = data.get('notes', '')
        items_data = data['items']

        delivery_zone = None
        delivery_charge = Decimal('60.00')
        if data.get('delivery_zone_id'):
            delivery_zone = DeliveryZone.objects.filter(id=data['delivery_zone_id'], is_active=True).first()
            if delivery_zone:
                delivery_charge = delivery_zone.delivery_charge

        order_number = cls.generate_order_number()
        
        # Calculate subtotal and build items
        subtotal = Decimal('0.00')
        prepared_items = []

        for item in items_data:
            product = Product.objects.select_related('category').get(id=item['product_id'])
            variant = None
            variant_weight = ''
            unit_price = Decimal(str(item['unit_price']))

            if item.get('variant_id'):
                variant = WeightVariant.objects.filter(id=item['variant_id']).first()
                if variant:
                    variant_weight = variant.weight
                    unit_price = Decimal(str(variant.price))
            
            quantity = item['quantity']
            item_total = unit_price * Decimal(quantity)
            subtotal += item_total

            prepared_items.append({
                'product': product,
                'variant': variant,
                'product_name': product.name,
                'variant_weight': variant_weight,
                'unit_price': unit_price,
                'quantity': quantity,
                'total_price': item_total
            })

        total_amount = subtotal + delivery_charge

        payment_status = 'pending_collection' if payment_method == 'COD' else 'pending'
        order_status = 'pending'

        # Create Order record
        order = Order.objects.create(
            order_number=order_number,
            user=user if user and user.is_authenticated else None,
            customer_name=customer_name,
            phone=phone,
            delivery_address=delivery_address,
            delivery_zone=delivery_zone,
            subtotal=subtotal,
            delivery_charge=delivery_charge,
            total_amount=total_amount,
            payment_method=payment_method,
            payment_status=payment_status,
            order_status=order_status,
            notes=notes
        )

        # Bulk create OrderItems
        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                product=item['product'],
                variant=item['variant'],
                product_name=item['product_name'],
                variant_weight=item['variant_weight'],
                unit_price=item['unit_price'],
                quantity=item['quantity'],
                total_price=item['total_price']
            ) for item in prepared_items
        ])

        return order
