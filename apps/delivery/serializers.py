from rest_framework import serializers
from .models import DeliveryZone


class DeliveryZoneSerializer(serializers.ModelSerializer):
    deliveryCharge = serializers.FloatField(source='delivery_charge', read_only=True)
    estimatedDeliveryTime = serializers.CharField(source='estimated_delivery_time', read_only=True)

    class Meta:
        model = DeliveryZone
        fields = [
            'id', 
            'area_name', 
            'city', 
            'delivery_charge', 
            'deliveryCharge',
            'estimated_delivery_time',
            'estimatedDeliveryTime', 
            'is_active'
        ]
