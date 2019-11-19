import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.status import is_success
from rest_framework.test import APITestCase

from warehouse.factories.storage import (
    StorageUnitFactory, StorageUnitComponentFactory
)
from warehouse.factories.warehouse import WarehouseComponentFactory


class StorageUnitTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            username='admin', email='admin@example.com',
            password='123', is_active=True
        )
        cls.storage_unit = StorageUnitFactory()
        cls.detail_url = reverse('storage-units-detail',
                                 kwargs={'pk': cls.storage_unit.pk})
        cls.list_url = reverse('storage-units-list')

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def _test_compare_objects(self, data):
        self.assertEqual(data['id'], self.storage_unit.id, data)
        self.assertEqual(data['name'], self.storage_unit.name, data)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertTrue(is_success(response.status_code))

        data = response.data
        self._test_compare_objects(data)

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertTrue(is_success(response.status_code))

        data = response.data[0]
        self._test_compare_objects(data)

    def test_create(self):
        data = {
            'name': 'TEST',
        }

        response = self.client.post(self.list_url, data=json.dumps(data),
                                    content_type='application/json'
                                    )

        self.assertTrue(is_success(response.status_code), response.data)
        data = response.data
        self.assertEqual(data['name'], 'TEST', data)

    def test_update(self):
        data = {
            'name': 'TEST123',
        }

        response = self.client.patch(self.detail_url, data=json.dumps(data),
                                     content_type='application/json')

        self.assertTrue(is_success(response.status_code))
        data = response.data
        self.assertEqual(data['name'], 'TEST123', data)


class StorageUnitComponentTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            username='admin', email='admin@example.com',
            password='123', is_active=True
        )
        cls.component = WarehouseComponentFactory()
        cls.storage_unit = StorageUnitFactory()
        cls.storage_unit_component = StorageUnitComponentFactory(
            component=cls.component, storage_unit=cls.storage_unit)

        cls.list_url = reverse('storage-unit-components-list')
        cls.detail_url = reverse(
            'storage-unit-components-detail',
            kwargs={'pk': cls.storage_unit_component.id}
        )

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        response_data = response.data

        self.assertTrue(is_success(response.status_code), response_data)

    def test_list(self):
        response = self.client.get(self.list_url)
        response_data = response.data

        self.assertTrue(is_success(response.status_code), response_data)
        self.assertGreaterEqual(len(response_data), 1, response_data)

    def test_create(self):
        component = WarehouseComponentFactory()
        data = {
            'storage_unit': self.storage_unit.id,
            'component': component.id,
            'quantity': 2,
        }

        response = self.client.post(self.list_url, data)

        self.assertTrue(is_success(response.status_code), response.data)

    def test_partial_update(self):
        pass
