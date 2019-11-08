from rest_framework import mixins, viewsets

from warehouse.models.storage import StorageUnit
from warehouse.serializers.storage import StorageUnitSerializer


class StorageUnitViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                         mixins.UpdateModelMixin, mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin):
    queryset = StorageUnit.objects.all()
    serializer_class = StorageUnitSerializer
