import datetime

from django.test import TestCase

from chore.factories import RentalPeriodFactory
from chore.models import RentalPeriod
from chore.services.rental_periods import RentalPeriodService


class RentalPeriodServiceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.start_datetime = datetime.datetime(2019, 11, 1, 0, 0, 0)
        cls.end_datetime = datetime.datetime(2019, 11, 10, 0, 0, 0)
        cls.r1 = RentalPeriodFactory(start_datetime=cls.start_datetime, end_datetime=cls.end_datetime)
        cls.r2 = RentalPeriodFactory(start_datetime=datetime.datetime(2019, 10, 20, 0, 0, 0),
                                     end_datetime=datetime.datetime(2019, 11, 5, 0, 0, 0))
        cls.r3 = RentalPeriodFactory(start_datetime=datetime.datetime(2019, 11, 8, 0, 0, 0),
                                     end_datetime=datetime.datetime(2019, 11, 20, 0, 0, 0))
        cls.r4 = RentalPeriodFactory(start_datetime=datetime.datetime(2019, 11, 9, 0, 0, 0),
                                     end_datetime=datetime.datetime(2019, 11, 22, 0, 0, 0))
        cls.r5 = RentalPeriodFactory(start_datetime=datetime.datetime(2019, 10, 31, 0, 0, 0),
                                     end_datetime=datetime.datetime(2019, 11, 15, 0, 0, 0))

    def test_rental_periods(self):
        service = RentalPeriodService(self.start_datetime, self.end_datetime)
        all_periods = [self.r1, self.r2, self.r3, self.r4, self.r5]
        for elem in all_periods:
            self.assertIn(elem, service.rental_periods)

    def test_get_overlapping(self):
        service = RentalPeriodService(self.start_datetime, self.end_datetime)
        expected_result = {
            self.r1.id: [self.r1.id, self.r2.id, self.r3.id, self.r4.id, self.r5.id],
            self.r2.id: [self.r1.id, self.r2.id, self.r5.id],
            self.r3.id: [self.r1.id, self.r3.id, self.r4.id, self.r5.id],
            self.r4.id: [self.r1.id, self.r3.id, self.r4.id, self.r5.id],
            self.r5.id: [self.r1.id, self.r2.id, self.r3.id, self.r4.id, self.r5.id],
        }

        self.assertEqual(service.get_overlapping(), expected_result, service.get_overlapping())
