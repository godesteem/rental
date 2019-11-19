from django_filters import rest_framework, DateFromToRangeFilter
from django_filters.widgets import RangeWidget
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

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
    date_range = DateFromToRangeFilter(
        widget=StartEndRangeWidget(attrs={'placeholder': 'DD-MM-YYYY'}),
        method='filter_date_range'
    )
    ids = rest_framework.BaseInFilter(field_name='id')
    status_in = rest_framework.BaseInFilter(field_name='status')

    class Meta:
        model = Product
        fields = {
            'status': ['exact'],
            'ids': ['exact'],
            'status_in': ['exact'],
        }

    def filter_date_range(self, queryset, name, value):
        service = AvailableProductsService(value.start, value.stop)
        return service.check_availability(queryset)


class ProductViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.UpdateModelMixin, mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_class = ProductFilter
    filterset_fields = ('status',)

    @action(detail=True, url_path='publish', methods=['post'])
    def publish(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        published = False
        if not product.status == product.PUBLISHED:
            product.publish()
            product.save(update_fields=['status'])
            published = True
        return Response(status=200, data={'published': published})
