from collections import OrderedDict

from rest_framework import serializers

from warehouse.models.storage import StorageUnit


class StorageUnitField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        from warehouse.serializers.storage import StorageUnitSerializer
        pk = super().to_representation(value)
        item = StorageUnit.objects.get(pk=pk)
        serializer = StorageUnitSerializer(item)
        return serializer.data

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        return OrderedDict([(item.id, str(item)) for item in queryset])
