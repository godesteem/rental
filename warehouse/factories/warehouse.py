import factory

from shop.factories.product import ProductFactory
from warehouse.models.warehouse import (
    WarehouseItem, WarehouseComponent, WarehouseItemComponent
)


class WarehouseItemFactory(factory.DjangoModelFactory):
    product = factory.SubFactory(ProductFactory)

    class Meta:
        model = WarehouseItem


class WarehouseComponentFactory(factory.DjangoModelFactory):
    name = factory.Faker('name')

    class Meta:
        model = WarehouseComponent


class WarehouseItemComponentFactory(factory.DjangoModelFactory):
    component = factory.SubFactory(WarehouseComponentFactory)
    item = factory.SubFactory(WarehouseItemFactory)

    class Meta:
        model = WarehouseItemComponent
