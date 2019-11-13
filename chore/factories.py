import datetime

import factory

from chore.models import RentalPeriod


class RentalPeriodFactory(factory.DjangoModelFactory):
    start_datetime = datetime.datetime(2019, 1, 1, 0, 0, 0)
    end_datetime = datetime.datetime(2019, 1, 10, 0, 0, 0)

    class Meta:
        model = RentalPeriod
