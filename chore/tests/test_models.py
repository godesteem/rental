import datetime

from django.test import TestCase
from parameterized import parameterized

from chore.factories import RentalPeriodFactory
from chore.models import RentalPeriod
from utils.test_clients import ModelStrTestCaseMixin


class RentalPeriodQuerySetTestCase(TestCase, ModelStrTestCaseMixin):
    obj = RentalPeriod(
        start_datetime=datetime.datetime(2019, 11, 1),
        end_datetime=datetime.datetime(2019, 11, 2)
    )
    string = '2019-11-01 00:00:00 -> 2019-11-02 00:00:00'

    @classmethod
    def setUpTestData(cls):
        cls.dates = [
            (datetime.datetime(2019, 11, 1, 0, 0, 0),
             datetime.datetime(2019, 11, 2, 0, 0, 0)),
            (datetime.datetime(2019, 10, 1, 0, 0, 0),
             datetime.datetime(2019, 10, 3, 0, 0, 0)),
            (datetime.datetime(2019, 12, 1, 0, 0, 0),
             datetime.datetime(2019, 12, 4, 0, 0, 0)),
            (datetime.datetime(2019, 1, 1, 0, 0, 0),
             datetime.datetime(2019, 1, 5, 0, 0, 0)),
            (datetime.datetime(2019, 1, 3, 0, 0, 0),
             datetime.datetime(2019, 1, 6, 0, 0, 0)),
        ]

        for dates in cls.dates:
            RentalPeriodFactory(start_datetime=dates[0],
                                end_datetime=dates[1])

    @parameterized.expand([
        (datetime.datetime(2019, 1, 1, 0, 0, 0),
         datetime.datetime(2019, 12, 31, 0, 0, 0), [0, 1, 2, 3, 4]),
        (datetime.datetime(2019, 10, 31, 0, 0, 0),
         datetime.datetime(2019, 11, 2, 0, 0, 0), [0]),
        (datetime.datetime(2019, 10, 31, 0, 0, 0),
         datetime.datetime(2019, 11, 5, 0, 0, 0), [0]),
        (datetime.datetime(2019, 11, 2, 0, 0, 0),
         datetime.datetime(2019, 11, 6, 0, 0, 0), [0]),
        (datetime.datetime(2019, 1, 2, 0, 0, 0),
         datetime.datetime(2019, 1, 4, 0, 0, 0), [3, 4]),
    ])
    def test_get_within(self, start_datetime, end_datetime,
                        expected_result_indexes):
        qs = RentalPeriod.objects.get_within(start_datetime,
                                             end_datetime)
        for index in expected_result_indexes:
            self.assertTrue(
                qs.filter(
                    start_datetime=self.dates[index][0],
                    end_datetime=self.dates[index][1]
                ).exists(),
                f'{self.dates[index][0]}, {self.dates[index][1]} '
                f'not in {start_datetime}, {end_datetime}'
            )
