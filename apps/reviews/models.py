import uuid
from django.db import models
from django.conf import settings
from apps.products.models import Product


class ProductReview(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_reviews'
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.phone} review on {self.product.name} ({self.rating}★)"
