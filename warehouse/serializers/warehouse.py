from django.db import transaction
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from shop.models import Product
from shop.serializers import ProductSerializer
from warehouse.models.warehouse import (
    WarehouseItem, WarehouseItemComponent, WarehouseComponent
)


class WarehouseComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseComponent
        fields = '__all__'


class WarehouseItemComponentSerializer(serializers.ModelSerializer):
    component = WarehouseComponentSerializer(read_only=True)
    component_id = serializers.IntegerField(write_only=True,
                                            source='component.id')

    class Meta:
        model = WarehouseItemComponent
        fields = ['id', 'component', 'quantity', 'component_id']


class WarehouseItemSerializer(serializers.ModelSerializer):
    warehouse_components = WarehouseItemComponentSerializer(
        many=True, read_only=True
    )
    product = ProductSerializer(read_only=True)
    warehouse_components_list = WarehouseItemComponentSerializer(
        many=True, write_only=True
    )
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = WarehouseItem
        fields = [
            'id', 'product', 'warehouse_components',
            'warehouse_components_list', 'product_id',
        ]

    def to_internal_value(self, data):
        if 'warehouse_components_list' in data:
            component_ids = [
                component['component_id']
                for component in data['warehouse_components_list']
            ]
            data['warehouse_components'] = WarehouseItemComponentSerializer(
                WarehouseComponent.objects.filter(id__in=component_ids),
                many=True
            )
        if 'product_id' in data:
            data['product'] = ProductSerializer(
                get_object_or_404(Product.objects.all(), pk=data['product_id'])
            )

        return super().to_internal_value(data)

    @staticmethod
    def update_or_create_components(components, instance):
        if components:
            for warehouse_component in components:
                WarehouseItemComponent.objects.update_or_create(
                    item=instance,
                    component_id=warehouse_component['component']['id'],
                    defaults={
                        'quantity': warehouse_component['quantity'],
                    }
                )

    @transaction.atomic
    def create(self, validated_data):
        warehouse_components = validated_data.pop(
            'warehouse_components_list'
        )
        product = validated_data.pop('product_id')
        if product is not None:
            validated_data['product'] = Product.objects.get(id=product)

        instance = super().create(validated_data)

        self.update_or_create_components(warehouse_components, instance)

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        warehouse_components = validated_data.pop(
            'warehouse_components_list', None
        )
        product = validated_data.pop('product_id', None)
        if product is not None:
            validated_data['product'] = Product.objects.get(id=product)

        instance = super().update(instance, validated_data)

        self.update_or_create_components(warehouse_components, instance)

        return instance
