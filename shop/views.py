from django_filters import rest_framework, DateFromToRangeFilter
from django_filters.widgets import RangeWidget
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAdminUser

from chore.services.available_products import AvailableProductsService
from shop.models import Order, Product
from shop.serializers import OrderSerializer, ProductSerializer


class OrderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]


class StartEndRangeWidget(RangeWidget):
    suffixes = ['start', 'end']


class ProductFilter(rest_framework.FilterSet):
    date_range = DateFromToRangeFilter(widget=StartEndRangeWidget(attrs={'placeholder': 'DD-MM-YYYY'}), method='filter_date_range')

    class Meta:
        model = Product
        fields = [
            'date_range'
        ]

    def filter_date_range(self, queryset, name, value):
        service = AvailableProductsService(value.start, value.stop)
        return service.check_availability(queryset)


class ProductViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.UpdateModelMixin, mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin):
    queryset = Product.objects.get_published()
    serializer_class = ProductSerializer
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_class = ProductFilter
