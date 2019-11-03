from django.urls import reverse
from rest_framework.status import is_success
from rest_framework.test import APITestCase

from shop.factories.product import ProductFactory
from shop.models import EUR


class OrderViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = ProductFactory()
        cls.list_url = reverse('products-list')
        cls.detail_url = reverse('products-detail',
                                 kwargs={'pk': cls.product.id})

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
