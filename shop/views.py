from rest_framework import mixins, viewsets

from shop.models import Order, Product
from shop.serializers import OrderSerializer, ProductSerializer


class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ProductViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.UpdateModelMixin, mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
