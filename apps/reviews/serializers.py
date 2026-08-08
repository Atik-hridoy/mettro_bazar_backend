from rest_framework import serializers
from .models import ProductReview


class ProductReviewSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source='user.name', read_only=True)
    userPhone = serializers.CharField(source='user.phone', read_only=True)
    isVerifiedPurchase = serializers.BooleanField(source='is_verified_purchase', read_only=True)

    class Meta:
        model = ProductReview
        fields = [
            'id', 
            'product', 
            'rating', 
            'comment', 
            'userName', 
            'userPhone', 
            'isVerifiedPurchase', 
            'is_verified_purchase',
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'is_verified_purchase', 'created_at']
