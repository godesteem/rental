import factory

from warehouse.models.storage import StorageUnit, StorageUnitComponent


class StorageUnitFactory(factory.DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = StorageUnit


class StorageUnitComponentFactory(factory.DjangoModelFactory):
    class Meta:
        model = StorageUnitComponent

