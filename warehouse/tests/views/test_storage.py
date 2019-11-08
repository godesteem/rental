import json

from django.urls import reverse
from rest_framework.status import is_success
from rest_framework.test import APITestCase

from warehouse.factories.storage import StorageUnitFactory


class StorageUnitTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.storage_unit = StorageUnitFactory()
        cls.detail_url = reverse('storage-units-detail', kwargs={'pk': cls.storage_unit.pk})
        cls.list_url = reverse('storage-units-list')

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
