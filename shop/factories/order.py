import factory
from django.contrib.auth import get_user_model

from shop.factories.product import ProductFactory
from shop.models import Address, Order, OrderItem


class UserFactory(factory.DjangoModelFactory):
    username = factory.Faker('name')

    class Meta:
        model = get_user_model()


class AddressFactory(factory.DjangoModelFactory):
    class Meta:
        model = Address


class OrderFactory(factory.DjangoModelFactory):
    customer = factory.SubFactory(UserFactory)
    delivery_address = factory.SubFactory(AddressFactory)
    payment_address = factory.SubFactory(AddressFactory)

    class Meta:
        model = Order


class OrderItemFactory(factory.DjangoModelFactory):
    product = factory.SubFactory(ProductFactory)
    order = factory.SubFactory(OrderFactory)
    quantity = 1

    class Meta:
        model = OrderItem
