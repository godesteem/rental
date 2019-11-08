import factory

from chore.models import RentalPeriod


class RentalPeriodFactory(factory.DjangoModelFactory):
    class Meta:
        model = RentalPeriod
