import factory

from shop.models import EUR, Product


class ProductFactory(factory.DjangoModelFactory):
    name = factory.Faker('word')
    price = 1000
    currency = EUR

    class Meta:
        model = Product


class PublishedProductFactory(ProductFactory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        instance = super()._create(model_class, *args, **kwargs)
        instance.publish()
        instance.save()
        return instance
