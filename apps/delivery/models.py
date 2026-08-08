import uuid
from django.db import models


class DeliveryZone(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    area_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default='Dhaka')
    delivery_charge = models.DecimalField(max_digits=8, decimal_places=2, default=60.00)
    estimated_delivery_time = models.CharField(max_length=100, default='30-45 mins')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'delivery_zones'
        verbose_name = 'Delivery Zone'
        verbose_name_plural = 'Delivery Zones'
        ordering = ['area_name']

    def __str__(self):
        return f"{self.area_name} ({self.city}) - ৳{self.delivery_charge}"
