from django.contrib import admin

from shop.models import Product, Address, Order, OrderItem

admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
