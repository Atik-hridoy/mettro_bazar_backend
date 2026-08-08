from rest_framework import viewsets, permissions
from .models import DeliveryZone
from .serializers import DeliveryZoneSerializer


class DeliveryZoneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryZone.objects.filter(is_active=True)
    serializer_class = DeliveryZoneSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
