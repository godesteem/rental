from rest_framework import serializers

from warehouse.models.storage import StorageUnit, StorageUnitComponent


class StorageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageUnit
        fields = '__all__'


class StorageUnitComponentSerializer(serializers.ModelSerializer):
    storage_unit = StorageUnitSerializer()

    class Meta:
        model = StorageUnitComponent
        fields = ['id', 'quantity', 'storage_unit', 'component']

    @staticmethod
    def _update_storage_unit(validated_data):
        storage_unit = validated_data.pop('storage_unit', None)
        if storage_unit:
            validated_data['storage_unit'] = StorageUnit.objects.get_or_create(**storage_unit)[0]
        return validated_data

    def create(self, validated_data):
        validated_data = self._update_storage_unit(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = self._update_storage_unit(validated_data)
        return super().update(instance, validated_data)
