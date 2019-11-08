from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAdminUser

from shop.models import Order, Product
from shop.serializers import OrderSerializer, ProductSerializer


class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]


class ProductViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.UpdateModelMixin, mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin):
    queryset = Product.objects.get_published()
    serializer_class = ProductSerializer
