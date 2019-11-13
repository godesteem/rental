import time
import unittest
from unittest import skipIf

from django.contrib.auth import get_user_model
from django.test import TestCase, tag
from django.test.runner import DiscoverRunner
from django.utils import timezone
from parameterized import parameterized

from chore.factories import RentalPeriodFactory
from chore.models import RentalPeriod
from chore.services.available_products import AvailableProductsService
from chore.services.rental_periods import RentalPeriodService
from shop.factories.order import OrderFactory, OrderItemFactory
from shop.factories.product import PublishedProductFactory
from shop.models import Product, OrderItem, Order
from warehouse.factories.storage import StorageUnitComponentFactory
from warehouse.factories.warehouse import WarehouseItemFactory, WarehouseItemComponentFactory
from warehouse.models.storage import StorageUnit, StorageUnitComponent
from warehouse.models.warehouse import WarehouseItem, WarehouseItemComponent, WarehouseComponent


@tag('big_dataset')
@skipIf(False, 'Ok.')
class BigDatasetTestCase(TestCase):
    dataset_len = 1000
    dataset_product_len = 2 * dataset_len

    @classmethod
    def setUpTestData(cls):
        print('Init test data.')
        cls.__clear_all()
        print('DB cleared')
        if cls.dataset_len == 1:
            cls._set_products()
            print('Products created')
        cls._set_rental_periods(12)
        print('RentalPeriods created')
        cls._set_orders()
        print('Orders created')
        cls.service = AvailableProductsService(timezone.datetime(2019, 10, 1, 0, 0, 0),
                                               timezone.datetime(2019, 12, 1, 0, 0, 0))

    @classmethod
    def __clear_all(cls):
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        RentalPeriod.objects.all().delete()
        get_user_model().objects.all().delete()
        if cls.dataset_len == 1:
            StorageUnitComponent.objects.all().delete()
            StorageUnit.objects.all().delete()
            WarehouseItemComponent.objects.all().delete()
            WarehouseComponent.objects.all().delete()
            WarehouseItem.objects.all().delete()
            Product.objects.all().delete()

    @classmethod
    def _set_rental_periods(cls, count):
        for i in range(count + 1):
            setattr(cls, f'rental_period{i}', RentalPeriodFactory(
                start_datetime=timezone.datetime(2019, 6 - (i % 6), 15 - (i % 15), 0, 0, 0),
                end_datetime=timezone.datetime(2019, 12 - (i % 6), 25 - (i % 10), 0, 0, 0)
            ))

    @classmethod
    def _set_orders(cls):
        for i in range(cls.dataset_len):
            setattr(cls, f'order{i}',
                    OrderFactory(
                        rental_period=getattr(cls, f'rental_period{i%(cls.dataset_len % 12)}')
                    ))
            setattr(cls, f'order_item{i}',
                    OrderItemFactory(
                        order=getattr(cls, f'order{i}'),
                        product=getattr(cls, f'product{i % cls.dataset_product_len}')
                    ))

    @classmethod
    def _set_products(cls):
        for i in range(cls.dataset_product_len):
            setattr(cls, f'product{i}',
                    PublishedProductFactory())
            setattr(cls, f'warehouse_item{i}',
                    WarehouseItemFactory(product=getattr(cls, f'product{i}'))
                    )
            setattr(cls, f'warehouse_item_component{i}',
                    WarehouseItemComponentFactory(
                        item=getattr(cls, f'warehouse_item{i}'), quantity=1
                    ))
            setattr(cls, f'storage_unit_component{i}',
                    StorageUnitComponentFactory(
                        component=getattr(cls, f'warehouse_item_component{i}').component, quantity=2
                    ))

    def test_setup_OK(self):
        start = time.time()
        self.assertGreaterEqual(Product.objects.all().count(), self.dataset_product_len)
        stop = time.time()
        print('Test took', stop - start)


class SimpleTest(BigDatasetTestCase):
    dataset_len = 100

    def test_availability(self):
        qs = self.service.check_availability(Product.objects.all())
        self.assertEqual(qs.count(), self.dataset_product_len)

    @parameterized.expand([
        ([timezone.datetime(2019, 1, 1, 0, 0, 0), timezone.datetime(2019, 12, 31, 0, 0, 0)], 'dataset_product_len'),
        ([timezone.datetime(2019, 1, 1, 0, 0, 0), timezone.datetime(2019, 1, 3, 0, 0, 0)], 'dataset_product_len'),
        ([timezone.datetime(2019, 1, 1, 0, 0, 0), timezone.datetime(2019, 1, 30, 0, 0, 0)], 'dataset_product_len'),
        ([timezone.datetime(2019, 1, 1, 0, 0, 0), timezone.datetime(2019, 3, 30, 0, 0, 0)], 'dataset_product_len'),
    ])
    def test_multi_availability(self, date_range, expected_count):
        if expected_count:
            expected_count = getattr(self, expected_count)
        service = AvailableProductsService(date_range[0], date_range[1])
        start = time.time()
        qs = service.check_availability(Product.objects.all())
        stop = time.time()
        print(stop - start)
        self.assertEqual(qs.count(), expected_count)


class ComplexTest(BigDatasetTestCase):
    dataset_len = 1
    dataset_product_len = 1

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.manipulate_products()
        cls.manipulate_orders()

    @classmethod
    def manipulate_orders(cls):
        # from 2020-05-01 –> 2020-05-10
        # ordered amount of products: 10
        rental_period, _ = RentalPeriod.objects.get_or_create(
            start_datetime=timezone.datetime(2020, 5, 1, 0, 0, 0),
            end_datetime=timezone.datetime(2020, 5, 10, 0, 0, 0)
        )
        order1 = OrderFactory(rental_period=rental_period)
        order2 = OrderFactory(rental_period=rental_period)

        OrderItemFactory(order=order1, product=cls.product0, quantity=6)
        OrderItemFactory(order=order2, product=cls.product0, quantity=4)

        cls.period_01 = rental_period

        # from 2020-06-01 –> 2020-06-10
        # ordered amount of products: 6
        rental_period, _ = RentalPeriod.objects.get_or_create(
            start_datetime=timezone.datetime(2020, 6, 1, 0, 0, 0),
            end_datetime=timezone.datetime(2020, 6, 10, 0, 0, 0)
        )
        order1 = OrderFactory(rental_period=rental_period)
        order2 = OrderFactory(rental_period=rental_period)
        order3 = OrderFactory(rental_period=rental_period)

        OrderItemFactory(order=order1, product=cls.product0, quantity=2)
        OrderItemFactory(order=order2, product=cls.product0, quantity=1)
        OrderItemFactory(order=order3, product=cls.product0, quantity=3)

        cls.period_02 = rental_period

        # reuse generated data to check performance
        # ordered amount of products: 8
        # 2019-05-01 –> 2019-05-10
        rental_period, _ = RentalPeriod.objects.get_or_create(
            start_datetime=timezone.datetime(2019, 5, 1, 0, 0, 0),
            end_datetime=timezone.datetime(2019, 5, 10, 0, 0, 0)
        )
        service = RentalPeriodService(rental_period.start_datetime, rental_period.end_datetime)

        # NOTE: we just set current rented quantity to 0
        # the calculation should take care of the rest

        OrderItem.objects.filter(product=cls.product0, order__rental_period__in=service.get_overlapping().keys()).update(quantity=0)
        order1 = OrderFactory(rental_period=rental_period)
        order2 = OrderFactory(rental_period=rental_period)

        OrderItemFactory(order=order1, product=cls.product0, quantity=6)
        OrderItemFactory(order=order2, product=cls.product0, quantity=2)

        cls.period_03 = rental_period

    @classmethod
    def manipulate_products(cls):
        StorageUnitComponent.objects.all().update(quantity=10)

    @parameterized.expand([
        ('period_01', 0),
        ('period_02', 4),
        ('period_03', 2),
    ])
    def test_case(self, period, expected_amount):
        rental_period = getattr(self, period)

        start = time.time()
        service = AvailableProductsService(rental_period.start_datetime, rental_period.end_datetime)
        stop = time.time()
        print('service init', stop - start)
        start = time.time()
        qs = service.check_availability(Product.objects.all())
        stop = time.time()
        print('qs generation', stop - start)
        if expected_amount > 0:
            self.assertEqual(qs.get(pk=self.product0.pk).available_quantity, expected_amount)
        else:
            self.assertNotIn(self.product0, qs)

    def test_case_3(self):
        rental_period = self.period_03
        start = time.time()
        service = AvailableProductsService(rental_period.start_datetime, rental_period.end_datetime)
        stop = time.time()
        print('service init', stop - start)
        start = time.time()
        qs = service.check_availability(Product.objects.all())
        stop = time.time()
        print('qs generation', stop - start)
        self.assertEqual(qs.get(pk=self.product0.pk).available_quantity, 2)

        with open('testdata.csv', 'a') as file:
            file.write(f'{self.dataset_len};{self.dataset_product_len};{stop - start}\n')

    @classmethod
    def tearDownClass(cls) -> None:
        pass


@skipIf(False, 'We really don\'t want this to run too often.')
class GenerateTestDataTest(TestCase):
    def test_generate(self):
        for i in range(1, 10000, 10):
            suite = unittest.TestSuite()
            test = ComplexTest
            test.dataset_len = i
            test.dataset_product_len = 300
            suite.addTest(test('test_case_3'))
            runner = DiscoverRunner()
            runner.run_suite(suite)
