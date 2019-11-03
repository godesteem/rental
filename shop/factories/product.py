import factory

from shop.models import EUR, Product


class ProductFactory(factory.DjangoModelFactory):
    name = factory.Faker('word')
    price = 1000
    currency = EUR

    class Meta:
        model = Product
