from django.contrib import admin
from django_fsm import TransitionNotAllowed

from shop.models import Address, Order, OrderItem, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status']
    readonly_fields = ['status']

    actions = ['make_publish']

    def make_publish(self, request, queryset):
        for obj in queryset:
            try:
                obj.publish()
            except TransitionNotAllowed:
                continue
            obj.save()

    make_publish.short_description = 'Publish selected products.'


admin.site.register(Product, ProductAdmin)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
