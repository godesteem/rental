from django.db import models


class WarehouseItem(models.Model):
    product = models.ForeignKey(to='shop.Product', on_delete=models.PROTECT, related_name='warehouse_items')
    components = models.ManyToManyField(to='warehouse.WarehouseComponent', through='warehouse.WarehouseItemComponent')


class WarehouseItemComponent(models.Model):
    item = models.ForeignKey(to=WarehouseItem, on_delete=models.PROTECT)
    component = models.ForeignKey(to='warehouse.WarehouseComponent', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)


class WarehouseComponent(models.Model):
    name = models.CharField(max_length=255)
    storage = models.ManyToManyField(to='warehouse.StorageUnit', through='warehouse.StorageUnitComponent')

    def __str__(self):
        return self.name
