from django.test import TestCase

from utils.test_clients import ModelStrTestCaseMixin
from warehouse.models.warehouse import WarehouseComponent


class WarehouseComponentTestCase(TestCase, ModelStrTestCaseMixin):
    obj = WarehouseComponent(name='A')
    string = 'A'
