import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from parameterized import parameterized
from rest_framework.status import is_success
from rest_framework.test import APITestCase

from chore.factories import RentalPeriodFactory
from shop.factories.order import OrderItemFactory, OrderFactory
from shop.factories.product import PublishedProductFactory
from shop.models import EUR
from warehouse.factories.storage import StorageUnitComponentFactory
from warehouse.factories.warehouse import WarehouseItemFactory, WarehouseItemComponentFactory


class ProductViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = PublishedProductFactory()
        cls.list_url = reverse('products-list')
        cls.detail_url = reverse('products-detail',
                                 kwargs={'pk': cls.product.id})
        cls.user = User.objects.create_superuser(
            username='admin', email='admin@example.com',
            password='123', is_active=True
        )

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_create(self):
        data = {
            'name': 'Test',
            'price': 1000,
            'currency': EUR,
        }

        response = self.client.post(self.list_url, data=data)

        self.assertTrue(is_success(response.status_code))
        response = response.data
        self.assertEqual(response['name'], 'Test')
        self.assertEqual(response['price'], 1000)
        self.assertEqual(response['currency'], EUR)

    def test_update(self):
        data = {
            'name': 'NEW Name'
        }

        response = self.client.patch(self.detail_url, data=data)

        self.assertTrue(is_success(response.status_code))
        response = response.data
        self.assertEqual(response['name'], 'NEW Name')

    def test_list(self):
        response = self.client.get(self.list_url)

        self.assertTrue(is_success(response.status_code))
        response = response.data
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['name'], self.product.name)
        self.assertEqual(response[0]['price'], self.product.price)
        self.assertEqual(response[0]['currency'], self.product.currency)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)

        self.assertTrue(is_success(response.status_code))
        response = response.data
        self.assertEqual(response['name'], self.product.name)
        self.assertEqual(response['price'], self.product.price)
        self.assertEqual(response['currency'], self.product.currency)

    def test_filter_date_range_working(self):
        kwargs = {'date_range_start': '2019-11-01', 'date_range_end': '2019-11-05'}

        response = self.client.get(self.list_url, data=kwargs)

        self.assertTrue(is_success(response.status_code))


class ProductFilterTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.list_url = reverse('products-list')
        cls.user = User.objects.create_superuser(
            username='admin', email='admin@example.com',
            password='123', is_active=True
        )
        cls.product = PublishedProductFactory()
        # 2019-11-01 –> 2019-11-02
        rental_period = RentalPeriodFactory(start_datetime=timezone.datetime(2019, 11, 1, 0, 0, 0),
                                            end_datetime=timezone.datetime(2019, 11, 2, 0, 0, 0))

        # 2019-01-01 –> 2019-01-05
        rental_period2 = RentalPeriodFactory(start_datetime=timezone.datetime(2019, 1, 1, 0, 0, 0),
                                             end_datetime=timezone.datetime(2019, 1, 5, 0, 0, 0))
        
        # 2019-01-04 –> 2019-02-01
        rental_period3 = RentalPeriodFactory(start_datetime=timezone.datetime(2019, 1, 4, 0, 0, 0),
                                             end_datetime=timezone.datetime(2019, 2, 1, 0, 0, 0))
        order = OrderFactory(rental_period=rental_period)
        order2 = OrderFactory(rental_period=rental_period2)
        order3 = OrderFactory(rental_period=rental_period3)
        OrderItemFactory(order=order, product=cls.product, quantity=2)
        OrderItemFactory(order=order2, product=cls.product, quantity=1)
        OrderItemFactory(order=order3, product=cls.product, quantity=1)
        warehouse_item = WarehouseItemFactory(product=cls.product)
        warehouse_item_component = WarehouseItemComponentFactory(
            item=warehouse_item, quantity=1)
        StorageUnitComponentFactory(
            component=warehouse_item_component.component, quantity=2)

    def setUp(self) -> None:
        self.client.force_login(self.user)

    @parameterized.expand([
        ({'date_range_start': '2019-11-01', 'date_range_end': '2019-11-05'}, False, 0),
        ({'date_range_start': '2019-10-01', 'date_range_end': '2019-10-05'}, True, 2),
        ({'date_range_start': '2019-01-01', 'date_range_end': '2019-01-05'}, False, 0),
        ({'date_range_start': '2019-01-24', 'date_range_end': '2019-01-30'}, True, 1),
    ])
    def test_filter_date_range(self, payload, expects_product, expected_count):
        response = self.client.get(self.list_url, data=payload)

        self.assertTrue(is_success(response.status_code))
        self.assertEqual(self.product.id in [i['id'] for i in response.data], expects_product, response.data)
        if expects_product:
            self.assertEqual(response.data[0]['available_quantity'], expected_count)
