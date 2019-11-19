import datetime

from django.test import TestCase
from parameterized import parameterized

from chore.factories import RentalPeriodFactory
from chore.services.available_products import AvailableProductsService
from shop.factories.order import OrderFactory, OrderItemFactory
from shop.factories.product import PublishedProductFactory
from shop.models import Product
from warehouse.factories.storage import (
    StorageUnitComponentFactory
)
from warehouse.factories.warehouse import (
    WarehouseItemFactory, WarehouseItemComponentFactory
)


class AvailableProductsServiceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rental_period = RentalPeriodFactory(
            start_datetime=datetime.datetime(2019, 11, 1, 0, 0, 0),
            end_datetime=datetime.datetime(2019, 11, 2, 0, 0, 0))
        cls.service = AvailableProductsService(
            datetime.datetime(2019, 10, 1, 0, 0, 0),
            datetime.datetime(2019, 12, 1, 0, 0, 0))
        cls.product = PublishedProductFactory()
        cls.product2 = PublishedProductFactory()
        cls.product3 = PublishedProductFactory()
        cls.order = OrderFactory(rental_period=cls.rental_period)
        cls.order_item = OrderItemFactory(
            order=cls.order, product=cls.product
        )
        cls.order_item = OrderItemFactory(
            order=cls.order, product=cls.product2
        )
        cls.order_item = OrderItemFactory(
            order=cls.order, product=cls.product3
        )
        cls.warehouse_item = WarehouseItemFactory(product=cls.product)
        cls.warehouse_item2 = WarehouseItemFactory(product=cls.product2)
        cls.warehouse_item3 = WarehouseItemFactory(product=cls.product3)
        cls.warehouse_item_component = WarehouseItemComponentFactory(
            item=cls.warehouse_item, quantity=1)
        cls.warehouse_item_component2 = WarehouseItemComponentFactory(
            item=cls.warehouse_item2, quantity=1)
        cls.warehouse_item_component3 = WarehouseItemComponentFactory(
            item=cls.warehouse_item3, quantity=1)
        cls.storage_unit_component = StorageUnitComponentFactory(
            component=cls.warehouse_item_component.component, quantity=2)
        cls.storage_unit_component2 = StorageUnitComponentFactory(
            component=cls.warehouse_item_component2.component, quantity=3)
        cls.storage_unit_component3 = StorageUnitComponentFactory(
            component=cls.warehouse_item_component3.component, quantity=1)

    def test_service_init(self):
        self.assertIn(self.rental_period, self.service.rental_periods)

    @parameterized.expand([
        ('product', 1),
        ('product2', 2),
        ('product3', 0),
    ])
    def test_check_availability(self, obj_name, expected_count):
        qs = self.service.check_availability(Product.objects.filter(
            pk=getattr(self, obj_name).id))
        if expected_count > 0:
            self.assertEqual(qs[0].available_quantity, expected_count)
        else:
            self.assertFalse(qs.exists())
