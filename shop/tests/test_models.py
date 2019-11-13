from django.test import TestCase

from shop.factories.order import AddressFactory, OrderFactory, OrderItemFactory
from shop.factories.product import ProductFactory
from shop.models import Product
from shop.order_fsm import OrderFSMModel
from utils.test_clients import ModelStrTestCaseMixin


class ProductNameTestCase(TestCase, ModelStrTestCaseMixin):
    obj = ProductFactory(name='A')
    string = 'A'


class AddressNameTestCase(TestCase, ModelStrTestCaseMixin):
    obj = AddressFactory()
    string = f'Address {obj.pk}'


class OrderNameTestCase(TestCase, ModelStrTestCaseMixin):
    obj = OrderFactory(customer__first_name='A', customer__last_name='B')
    string = f'{obj.pk}: A B ({obj.created_at})'


class OrderItemNameTestCase(TestCase, ModelStrTestCaseMixin):
    obj = OrderItemFactory()
    string = f'{obj.order.id} – {obj.product.name} (x {obj.quantity})'


class OrderFSMModelNameTestCase(TestCase, ModelStrTestCaseMixin):
    obj = OrderFSMModel()
    string = OrderFSMModel.NEW


class ProductModelTestCase(TestCase):
    def setUp(self) -> None:
        self.product = ProductFactory()

    def test_publish(self):
        self.product.publish()
        self.product.save()
        self.assertEqual(self.product.status, Product.PUBLISHED)

    def test_unpublish(self):
        self.product.publish()
        self.product.save()
        self.assertEqual(self.product.status, Product.PUBLISHED)
        self.product.unpublish()
        self.product.save()
        self.assertEqual(self.product.status, Product.DRAFT)
