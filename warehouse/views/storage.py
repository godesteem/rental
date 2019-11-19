from rest_framework import mixins, viewsets

from warehouse.models.storage import StorageUnit, StorageUnitComponent
from warehouse.serializers.storage import (
    StorageUnitSerializer, StorageUnitComponentSerializer
)


class StorageUnitViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                         mixins.UpdateModelMixin, mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin):
    queryset = StorageUnit.objects.all()
    serializer_class = StorageUnitSerializer


class StorageUnitComponentViewSet(viewsets.GenericViewSet,
                                  mixins.ListModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.CreateModelMixin,
                                  mixins.RetrieveModelMixin):
    queryset = StorageUnitComponent.objects.all()
    serializer_class = StorageUnitComponentSerializer
