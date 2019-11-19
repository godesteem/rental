import datetime
import typing

from django.db.models import QuerySet, F, Sum, Case, When

from chore.services.rental_periods import RentalPeriodService


class AvailableProductsService:
    def __init__(self, from_date: datetime.datetime,
                 to_date: datetime.datetime) -> None:
        self.from_date = from_date
        self.to_date = to_date
        self.rental_period_service = RentalPeriodService(
            self.from_date, self.to_date)

    @property
    def rental_periods(self) -> QuerySet:
        return self.rental_period_service.rental_periods

    def check_availability(self, products: QuerySet) -> QuerySet:
        return self.__get_available_products(products)

    @staticmethod
    def __annotate_storage(products) -> QuerySet:
        annotation = Sum(
            F('warehouse_item__components__storage_units__quantity')
        ) / Sum(
            F('warehouse_item__warehouse_components__quantity')
        )
        return products.filter(
            warehouse_item__warehouse_components__isnull=False
        ).annotate(
            quantity_in_stock=annotation
        )

    def __annotate_ordered(self, products):
        rented_products = self.__get_rented_products_quantity(products)
        whens = [
            When(id=key, then=F('quantity_in_stock') - value)
            for key, value in rented_products.items()
        ]
        return products.annotate(
            available_quantity=Case(
                *whens,
                default=F('quantity_in_stock'),
            )
        )

    def __get_available_products(self, products: QuerySet) -> QuerySet:
        products = self.__annotate_storage(products)
        products = self.__annotate_ordered(products)
        return products.filter(available_quantity__gt=0)

    def __get_rented_products_quantity(self, products) -> typing.Dict:
        """calculates the maximum of rented amount per product"""
        overlapping_periods = self.rental_period_service.get_overlapping()
        return {elem.id: max(
            [
                sum(elem.order_items.filter(
                    order__rental_period__in=rental_periods
                ).values_list('quantity', flat=True))
                for rental_periods in overlapping_periods.values()
            ] + [0]) for elem in products}
