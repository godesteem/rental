from django.test import TestCase
from parameterized import parameterized
from rest_framework.exceptions import ValidationError

from warehouse.factories.storage import StorageUnitFactory, StorageUnitComponentFactory
from warehouse.factories.warehouse import WarehouseComponentFactory
from warehouse.models.storage import StorageUnit
from warehouse.serializers.fields import StorageUnitField


class StorageUnitFieldTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.component = WarehouseComponentFactory()
        cls.storage_unit = StorageUnitFactory()
        cls.storage_unit_component = StorageUnitComponentFactory(
            component=cls.component, storage_unit=cls.storage_unit)

    def test_get_choices(self):
        field = StorageUnitField(queryset=StorageUnit.objects.all())
        choices = [(i, y) for i, y in field.get_choices().items()]
        self.assertIn((self.storage_unit.id, str(self.storage_unit)), choices)

    def test_get_choices_qs_none(self):
        field = StorageUnitField(queryset=None, read_only=True)
        self.assertEqual(field.get_choices(), {})

    def test_get_choices_empty_qs(self):
        field = StorageUnitField(queryset=StorageUnit.objects.none())
        self.assertEqual(field.get_choices(), {})

    def test_to_representation(self):
        component_id = self.storage_unit.id
        field = StorageUnitField(queryset=StorageUnit.objects.all())
        internal_value = field.to_internal_value(component_id)

        self.assertEqual(internal_value, self.storage_unit)

    def test_to_representation_fail(self):
        field = StorageUnitField(queryset=StorageUnit.objects.all())
        with self.assertRaises(ValidationError):
            field.to_internal_value(0)
