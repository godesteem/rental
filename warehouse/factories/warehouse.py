import factory

from warehouse.models.warehouse import WarehouseItem, WarehouseComponent, WarehouseItemComponent


class WarehouseItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = WarehouseItem


class WarehouseItemComponentFactory(factory.DjangoModelFactory):
    class Meta:
        model = WarehouseItemComponent


class WarehouseComponentFactory(factory.DjangoModelFactory):
    name = factory.Faker('name')

    class Meta:
        model = WarehouseComponent
