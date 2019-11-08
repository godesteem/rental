from rest_framework import serializers

from warehouse.models.storage import StorageUnit, StorageUnitComponent


class StorageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageUnit
        fields = '__all__'


class StorageUnitComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageUnitComponent
        fields = '__all__'
