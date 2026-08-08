from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_spectacular.utils import extend_schema
from .models import UserAddress
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer, UserAddressSerializer
from .services import AuthService


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=LoginSerializer, responses={200: dict})
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        success, data = AuthService.login_user(
            phone=serializer.validated_data['phone'],
            password=serializer.validated_data['password']
        )

        if not success:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=RegisterSerializer, responses={201: dict})
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success, data = AuthService.register_user(data=serializer.validated_data)

        if not success:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @extend_schema(responses={200: UserSerializer})
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    @extend_schema(request=UserSerializer, responses={200: UserSerializer})
    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserAddressViewSet(viewsets.ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework import generics
from django.contrib.auth import get_user_model

class AdminUserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = None

    def get_queryset(self):
        return get_user_model().objects.all().order_by('-created_at')
