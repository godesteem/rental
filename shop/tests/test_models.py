from django.test import TestCase

from shop.factories.order import AddressFactory, OrderFactory, OrderItemFactory
from shop.factories.product import ProductFactory


class ModelStrTestCaseMixin:
    obj = None
    string = ''

    def test_str(self):
        self.assertEqual(self.obj.__str__(), self.string)


class ProductNameTestCase(TestCase, ModelStrTestCaseMixin):
    obj = ProductFactory(name='A')
    string = 'A'


class AddressNameTestCase(TestCase, ModelStrTestCaseMixin):
    obj = AddressFactory()
    string = f'Address {obj.pk}'


class OrderNameTestCase(TestCase, ModelStrTestCaseMixin):
    obj = OrderFactory()
    string = f'{obj.pk}: {obj.customer.get_full_name} ({obj.created_at})'


class OrderItemNameTestCase(TestCase, ModelStrTestCaseMixin):
    obj = OrderItemFactory()
    string = f'{obj.order.id} – {obj.product.name} (x {obj.quantity})'
