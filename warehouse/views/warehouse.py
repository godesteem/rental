from rest_framework import viewsets, mixins

from warehouse.models.warehouse import WarehouseItem
from warehouse.serializers.warehouse import WarehouseItemSerializer


class WarehouseItemViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                           mixins.UpdateModelMixin, mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin):
    queryset = WarehouseItem.objects.all()
    serializer_class = WarehouseItemSerializer
