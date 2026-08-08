from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from apps.orders.models import Order
from .serializers import SSLCommerzInitSerializer, TransactionSerializer
from .services import SSLCommerzService


class SSLCommerzInitView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=SSLCommerzInitSerializer, responses={200: dict})
    def post(self, request, *args, **kwargs):
        serializer = SSLCommerzInitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order_id = serializer.validated_data['order_id']
        order = Order.objects.filter(id=order_id).first() or Order.objects.filter(order_number=order_id).first()

        if not order:
            return Response({"detail": f"Order {order_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        res = SSLCommerzService.init_payment(order=order, request=request)
        if res.get('status') == 'SUCCESS':
            return Response(res, status=status.HTTP_200_OK)
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class SSLCommerzWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(responses={200: dict})
    def post(self, request, *args, **kwargs):
        ipn_data = request.data or request.POST.dict()
        success, message = SSLCommerzService.verify_and_process_ipn(ipn_data)

        if success:
            return Response({"status": "SUCCESS", "detail": message}, status=status.HTTP_200_OK)
        return Response({"status": "ERROR", "detail": message}, status=status.HTTP_400_BAD_REQUEST)
