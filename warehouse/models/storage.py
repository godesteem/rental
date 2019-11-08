from django.db import models


class StorageUnitComponent(models.Model):
    storage_unit = models.ForeignKey(to='warehouse.StorageUnit', on_delete=models.PROTECT,
                                     related_name='components')
    component = models.ForeignKey(to='warehouse.WarehouseComponent', on_delete=models.PROTECT,
                                  related_name='storage_units')
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'({str(self.__class__.__name__)}) {self.storage_unit}: {self.component} x {self.quantity}'


class StorageUnit(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
