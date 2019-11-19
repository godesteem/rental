import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.status import is_success
from rest_framework.test import APITestCase

from shop.factories.product import ProductFactory
from warehouse.factories.warehouse import (
    WarehouseItemFactory, WarehouseItemComponentFactory,
    WarehouseComponentFactory,
)


class WarehouseItemTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            username='admin', email='admin@example.com',
            password='123', is_active=True
        )
        cls.product = ProductFactory()
        cls.item = WarehouseItemFactory(product=cls.product)
        warehouse_item_component = WarehouseItemComponentFactory(
            item=cls.item, quantity=2
        )
        cls.component = warehouse_item_component.component
        cls.detail_url = reverse('warehouse-items-detail',
                                 kwargs={'pk': cls.product.pk})
        cls.list_url = reverse('warehouse-items-list')

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def _test_compare_objects(self, data, item, product):
        self.assertEqual(data['id'], item.id, data)
        self.assertEqual(data['product']['id'], product.id, data)
        self.assertEqual(data['product']['name'], product.name, data)
        self.assertEqual(data['warehouse_components'][0]['component']['name'],
                         self.component.name)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertTrue(is_success(response.status_code))

        data = response.data
        self._test_compare_objects(data, self.item, self.product)

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertTrue(is_success(response.status_code))

        data = response.data[0]
        self._test_compare_objects(data, self.item, self.product)

    def test_create(self):
        product = ProductFactory()
        component = WarehouseComponentFactory()
        data = {
            'product_id': product.id,
            'warehouse_components_list': [
                {'component_id': component.id, 'quantity': 2}
            ],
        }

        response = self.client.post(self.list_url, data=json.dumps(data),
                                    content_type='application/json'
                                    )
        self.assertTrue(is_success(response.status_code), response.data)

        data = response.data

        self.assertEqual(data['product']['id'], product.id, data)
        self.assertEqual(data['product']['name'], product.name, data)
        self.assertEqual(data['warehouse_components'][0]['component']['name'],
                         component.name, data)

    def test_update(self):
        product = ProductFactory()
        WarehouseItemFactory(product=product)
        detail_url = reverse('warehouse-items-detail',
                             kwargs={'pk': product.pk})
        data = {
            'warehouse_components_list': [
                {'component_id': self.component.id, 'quantity': 3}
            ],
            'product_id': product.id,
        }

        response = self.client.patch(detail_url, data=json.dumps(data),
                                     content_type='application/json')

        self.assertTrue(is_success(response.status_code))

        data = response.data

        self.assertEqual(data['warehouse_components'][0]['quantity'], 3, data)
        self.assertEqual(data['product']['id'], product.id, data)


class WarehouseComponentViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            username='admin', email='admin@example.com',
            password='123', is_active=True
        )
        cls.product = ProductFactory()
        cls.item = WarehouseItemFactory(product=cls.product)
        warehouse_item_component = WarehouseItemComponentFactory(
            item=cls.item, quantity=2
        )
        cls.component = warehouse_item_component.component
        cls.list_url = reverse('warehouse-components-list')
        cls.detail_url = reverse(
            'warehouse-components-detail',
            kwargs={'pk': cls.component.id}
        )

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_list(self):
        response = self.client.get(self.list_url)
        data = response.data

        self.assertTrue(is_success(response.status_code), data)
        self.assertGreaterEqual(len(data), 1, data)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        data = response.data

        self.assertTrue(is_success(response.status_code), data)
        self.assertEqual(data['id'], self.component.id)
        self.assertEqual(data['name'], self.component.name)

    def test_create(self):
        data = {
            'name': 'TEST Component'
        }

        response = self.client.post(self.list_url, data)
        response_data = response.data

        self.assertTrue(is_success(response.status_code), response_data)
