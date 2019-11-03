from django.contrib import admin

from shop.models import Address, Order, OrderItem, Product

admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
