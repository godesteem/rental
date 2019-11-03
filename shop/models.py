from django.contrib.auth import get_user_model
from django.db import models

from shop.order_fsm import OrderFSMMixin

EUR = 'EUR'
USD = 'USD'
CURRENCIES = [(EUR, 'Euro'), (USD, 'USD')]


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    currency = models.CharField(choices=CURRENCIES, default=EUR, max_length=3)

    def __str__(self):
        return self.name


class Address(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=25)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    note = models.TextField()

    def __str__(self):
        return f'Address {self.pk}'


class Order(models.Model, OrderFSMMixin):
    customer = models.ForeignKey(to=get_user_model(), on_delete=models.PROTECT)
    delivery_address = models.ForeignKey(to=Address, on_delete=models.PROTECT, blank=True, null=True,
                                         related_name='order_deliveryaddress')
    payment_address = models.ForeignKey(to=Address, on_delete=models.PROTECT, blank=True, null=True,
                                        related_name='order_paymentaddress')
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    price = models.IntegerField()
    currency = models.CharField(choices=CURRENCIES, default=EUR, max_length=3)

    def __str__(self):
        return f'{self.pk}: {self.customer.full_name} ({self.created_at})'


class OrderItem(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT)
    order = models.ForeignKey(to=Order, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.order.id} – {self.product.name} (x {self.quantity})'
