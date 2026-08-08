from rest_framework import viewsets, permissions
from .models import ProductReview
from .serializers import ProductReviewSerializer


class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all().select_related('user', 'product')
    serializer_class = ProductReviewSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
