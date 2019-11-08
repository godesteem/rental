from django.test import TestCase

from shop.factories.product import ProductFactory
from utils.test_clients import ModelStrTestCaseMixin
from warehouse.factories.storage import StorageUnitFactory
from warehouse.factories.warehouse import WarehouseComponentFactory, WarehouseItemFactory
from warehouse.models.storage import StorageUnitComponent, StorageUnit
from warehouse.models.warehouse import WarehouseComponent, WarehouseItem, WarehouseItemComponent

product = ProductFactory()
storage_unit = StorageUnitFactory()
warehouse_component = WarehouseComponentFactory()
warehouse_item = WarehouseItemFactory(product=product)


class WarehouseComponentTestCase(TestCase, ModelStrTestCaseMixin):
    obj = WarehouseComponent(name='A')
    string = 'A'


class WarehouseItemTestCase(TestCase, ModelStrTestCaseMixin):
    obj = WarehouseItem(product=product)
    string = product.__str__()


class WarehouseItemComponentTestCase(TestCase, ModelStrTestCaseMixin):
    obj = WarehouseItemComponent(item=warehouse_item, component=warehouse_component, quantity=2)
    string = f'({str(WarehouseItemComponent.__name__)}) {warehouse_item}: {warehouse_component.name} x 2'


class StorageUnitComponentTestCase(TestCase, ModelStrTestCaseMixin):
    obj = StorageUnitComponent(storage_unit=storage_unit, component=warehouse_component, quantity=2)
    string = f'({str(StorageUnitComponent.__name__)}) {storage_unit.name}: {warehouse_component.name} x 2'


class StorageUnitTestCase(TestCase, ModelStrTestCaseMixin):
    obj = StorageUnit(name='A')
    string = 'A'
