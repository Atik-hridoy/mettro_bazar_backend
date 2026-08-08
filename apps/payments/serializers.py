from rest_framework import serializers
from .models import Transaction


class SSLCommerzInitSerializer(serializers.Serializer):
    order_id = serializers.CharField(required=True)


class TransactionSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 
            'order_id', 
            'order_number', 
            'tran_id', 
            'val_id', 
            'amount', 
            'currency', 
            'card_type', 
            'status', 
            'created_at'
        ]
