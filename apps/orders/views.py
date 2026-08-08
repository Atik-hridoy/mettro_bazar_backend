from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Order, Cart, CartItem
from .serializers import (
    OrderCreateSerializer, 
    OrderListSerializer, 
    OrderDetailSerializer,
    CartSerializer
)
from .services import OrderService


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('items')
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        # If user is authenticated customer, filter to user's orders unless staff
        if self.request.user and self.request.user.is_authenticated:
            if not self.request.user.is_staff:
                return queryset.filter(user=self.request.user)
            return queryset
        # Guest user query by phone if provided in query params
        phone = self.request.query_params.get('phone')
        if phone:
            return queryset.filter(phone=phone)
        return queryset.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderListSerializer

    @extend_schema(request=OrderCreateSerializer, responses={201: OrderDetailSerializer})
    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order = OrderService.create_order(
            user=request.user if request.user.is_authenticated else None,
            data=serializer.validated_data
        )

        response_serializer = OrderDetailSerializer(order, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CartSyncView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(responses={200: CartSerializer})
    def post(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        session_id = request.data.get('session_id', '')

        if user:
            cart, _ = Cart.objects.get_or_create(user=user)
        else:
            cart, _ = Cart.objects.get_or_create(session_id=session_id or 'guest-cart')

        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
