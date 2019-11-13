import json

from django.contrib.auth.models import User
from django.urls import reverse
from parameterized import parameterized
from rest_framework.status import is_success
from rest_framework.test import APITestCase

from chore.factories import RentalPeriodFactory
from shop.factories.order import OrderFactory, OrderItemFactory, UserFactory
from shop.factories.product import PublishedProductFactory
from shop.models import EUR


class OrderViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.order = OrderFactory()
        cls.order_item = OrderItemFactory(order=cls.order)
        cls.list_url = reverse('orders-list')
        cls.detail_url = reverse('orders-detail', kwargs={'pk': cls.order.id})
        cls.address_dict = {
            'first_name': 'A',
            'last_name': 'B',
            'address_line_1': 'C',
            'address_line_2': 'D',
            'zip_code': 'E',
            'city': 'F',
            'country': 'G',
            'note': 'SOME NOTE',
        }
        cls.product = PublishedProductFactory(name='Product 2', price=1000,
                                              currency=EUR)
        cls.order_items_list = [{'product': {
            'name': 'Product 2', 'price': 1000, 'currency': EUR
        }, 'quantity': 1}]
        cls.rental_period_dict = {
            'start_datetime': '2019-01-01T00:00:00Z',
            'end_datetime': '2019-01-10T00:00:00Z',
        }
        cls.user = User.objects.create_superuser(
            username='admin', email='admin@example.com',
            password='123', is_active=True
        )

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_list(self):
        response = self.client.get(self.list_url)

        self.assertTrue(is_success(response.status_code))
        response = response.data
        self.assertEqual(len(response), 1)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)

        self.assertTrue(is_success(response.status_code))
        response = response.data

        self.assertEqual(
            self.order_item.id, response['order_items'][0]['id'])

    def test_create(self):
        delivery_address = self.address_dict
        payment_address = {
            'first_name': 'a',
            'last_name': 'b',
            'address_line_1': 'c',
            'address_line_2': 'd',
            'zip_code': 'e',
            'city': 'f',
            'country': 'g',
            'note': 'some note',
        }
        customer = UserFactory()
        data = {
            'payment_address': payment_address,
            'delivery_address': delivery_address,
            'customer': customer.id,
            'order_items': self.order_items_list,
            'rental_period': self.rental_period_dict,
        }

        response = self.client.post(
            self.list_url, data=json.dumps(data),
            content_type='application/json'
        )

        self.assertTrue(is_success(response.status_code), response.data)
        response = response.data
        self.assertEqual(
            response['delivery_address']['first_name'],
            delivery_address['first_name'])
        self.assertEqual(
            response['payment_address']['first_name'],
            payment_address['first_name'])
        self.assertEqual(
            response['customer'], customer.id)
        self.assertEqual(
            response['order_items'][0]['product']['id'], self.product.id)

    @parameterized.expand([
        ('delivery_address', 'address_dict', True),
        ('payment_address', 'address_dict', True),
        ('order_items', 'order_items_list', False),
        ('rental_period', 'rental_period_dict', True),
    ])
    def test_update(self, field_name, data_dict_name, expects_dict):
        data_dict = getattr(self, data_dict_name)
        data = {
            field_name: data_dict,
        }

        response = self.client.patch(
            self.detail_url,
            data=json.dumps(data), content_type='application/json')

        self.assertTrue(is_success(response.status_code), response.data)
        field = response.data[field_name]
        if expects_dict:
            for elem in data_dict.keys():
                self.assertEqual(field[elem], data_dict[elem])
        else:
            for elem in data_dict:
                self.assertIn(elem, data_dict)
