from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import F,Sum

from . import models
from . import serializers


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def add_stock(self, request,pk=None):
        product = self.get_object()
        quantity = int(request.data.get('quantity', 0))
        reason = request.data.get('reason')
        product.quantity += quantity
        product.save()

        models.StockLog.objects.create(
            product=product,
            quantity_changed=quantity,
            reason=reason
        )

        return Response({'status': 'stock added'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def remove_stock(self, request,pk=None):
        product = self.get_object()
        quantity = int(request.data.get('quantity', 0))
        reason = request.data.get('reason')
        if product.quantity < quantity:
            return Response({"status": "Invalid quantity"})
        product.quantity -= quantity
        product.save()

        models.StockLog.objects.create(
            product=product,
            quantity_changed=-quantity,
            reason=reason
        )

        return Response({'status': 'stock removed'})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def low_stock_alerts(self, request):
        low_stock_products = models.Product.objects.filter(quantity__lt=F('threshold'))
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def report_total_value(self, request):
        total_value = models.Product.objects.aggregate(total_value=Sum(F('quantity') * F('price')))['total_value']

        return Response({
            'total_inventory_value': total_value,
        })

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def sort_by_stock(self, request):
        product_query_params = request.query_params.get('product', 'asc')

        if product_query_params == 'desc':
            products = models.Product.objects.all().order_by('-quantity')
        else:
            products = models.Product.objects.all().order_by('quantity')

        serializer = self.get_serializer(products, many=True)

        return Response(serializer.data)