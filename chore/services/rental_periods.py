import datetime
import typing

from chore.models import RentalPeriod, RentalPeriodQuerySet


class RentalPeriodService:
    def __init__(self, from_date: datetime.datetime,
                 to_date: datetime.datetime) -> None:
        self.from_date = from_date
        self.to_date = to_date

    @property
    def rental_periods(self) -> RentalPeriodQuerySet:
        return RentalPeriod.objects.all().get_within(
            self.from_date, self.to_date)

    def get_overlapping(self) -> typing.Dict:
        """Builds the graph of overlapping RentalPeriods"""
        return {elem.id: list(
            self.rental_periods.get_within(
                elem.start_datetime,
                elem.end_datetime
            ).values_list('pk', flat=True)
        ) for elem in self.rental_periods}
