from django.db import models


class WarehouseItem(models.Model):
    product = models.OneToOneField(
        to='shop.Product', on_delete=models.PROTECT,
        related_name='warehouse_item'
    )
    components = models.ManyToManyField(
        to='warehouse.WarehouseComponent',
        through='warehouse.WarehouseItemComponent'
    )

    def __str__(self):
        return str(self.product)


class WarehouseItemComponent(models.Model):
    item = models.ForeignKey(
        to=WarehouseItem, on_delete=models.PROTECT,
        related_name='warehouse_components'
    )
    component = models.ForeignKey(
        to='warehouse.WarehouseComponent',
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'({str(self.__class__.__name__)}) ' \
            f'{self.item.product.name}: ' \
            f'{self.component.name} ' \
            f'x {self.quantity}'


class WarehouseComponent(models.Model):
    name = models.CharField(max_length=255)
    storage = models.ManyToManyField(
        to='warehouse.StorageUnit',
        through='warehouse.StorageUnitComponent'
    )

    def __str__(self):
        return self.name
