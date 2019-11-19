from rest_framework import serializers

from warehouse.models.storage import StorageUnit, StorageUnitComponent
from warehouse.serializers.fields import StorageUnitField


class StorageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageUnit
        fields = '__all__'


class StorageUnitComponentSerializer(serializers.ModelSerializer):
    storage_unit = StorageUnitField(queryset=StorageUnit.objects.all())

    class Meta:
        model = StorageUnitComponent
        fields = ['id', 'quantity', 'storage_unit', 'component']
