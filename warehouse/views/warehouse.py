from rest_framework import viewsets, mixins

from warehouse.models.warehouse import WarehouseItem, WarehouseComponent
from warehouse.serializers.warehouse import WarehouseItemSerializer, WarehouseComponentSerializer


class WarehouseItemViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                           mixins.UpdateModelMixin, mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin):
    queryset = WarehouseItem.objects.all()
    serializer_class = WarehouseItemSerializer

    def get_object(self):
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {'product_id': self.kwargs[lookup_url_kwarg]}
        obj, _ = WarehouseItem.objects.get_or_create(**filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class WarehouseComponentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                                mixins.UpdateModelMixin, mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin):
    queryset = WarehouseComponent.objects.all()
    serializer_class = WarehouseComponentSerializer
