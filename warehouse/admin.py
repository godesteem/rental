from django.contrib import admin

from warehouse.models.storage import StorageUnitComponent, StorageUnit
from warehouse.models.warehouse import (
    WarehouseItemComponent, WarehouseItem, WarehouseComponent
)


class WarehouseItemComponentInline(admin.TabularInline):
    model = WarehouseItemComponent
    extra = 0


class StorageUnitComponentInline(admin.TabularInline):
    model = StorageUnitComponent
    extra = 0


class WarehouseComponentAdmin(admin.ModelAdmin):
    inlines = [StorageUnitComponentInline]


class WarehouseItemAdmin(admin.ModelAdmin):
    inlines = [WarehouseItemComponentInline]
    fields = ['product']


admin.site.register(WarehouseItem, WarehouseItemAdmin)
admin.site.register(WarehouseComponent, WarehouseComponentAdmin)
admin.site.register(StorageUnit)
admin.site.register(StorageUnitComponent)
