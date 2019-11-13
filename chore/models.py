import datetime

from django.db import models


class RentalPeriodQuerySet(models.QuerySet):
    def get_within(
            self, start_datetime: datetime.datetime,
            end_datetime: datetime.datetime) -> 'RentalPeriodQuerySet':
        return self.filter(
            models.Q(start_datetime__range=(start_datetime, end_datetime))
            | models.Q(end_datetime__range=(start_datetime, end_datetime))
            | models.Q(
                start_datetime__lte=start_datetime,
                end_datetime__gte=end_datetime
            )
        )


class RentalPeriodManager(models.Manager):
    def get_queryset(self):
        return RentalPeriodQuerySet(self.model, using=self._db)


class RentalPeriod(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    objects = RentalPeriodManager()

    @staticmethod
    def validate_dates(start_datetime: datetime.datetime,
                       end_datetime: datetime.datetime) -> None:
        assert start_datetime < end_datetime, \
            'start_datetime is not before end_datetime'

    def save(self, *args, **kwargs):
        if self.start_datetime and self.end_datetime:
            self.validate_dates(self.start_datetime, self.end_datetime)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.start_datetime} -> {self.end_datetime}'
