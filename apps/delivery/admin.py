from django.contrib import admin
from .models import DeliveryZone


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'city', 'delivery_charge', 'estimated_delivery_time', 'is_active')
    list_filter = ('city', 'is_active')
    search_fields = ('area_name', 'city')
