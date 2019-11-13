from django.contrib.auth import get_user_model
from django.db import models
from django_fsm import FSMField, transition

from shop.order_fsm import OrderFSMModel

EUR = 'EUR'
USD = 'USD'
CURRENCIES = [(EUR, 'Euro'), (USD, 'USD')]


class ProductManager(models.Manager):
    def get_published(self):
        return super().get_queryset().filter(status=Product.PUBLISHED)


class Product(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    currency = models.CharField(choices=CURRENCIES, default=EUR, max_length=3)
    status = FSMField(default=DRAFT, protected=True, choices=STATES)

    objects = ProductManager()

    @transition(field=status, source=DRAFT, target=PUBLISHED)
    def publish(self):
        pass

    @transition(field=status, source=PUBLISHED, target=DRAFT)
    def unpublish(self):
        pass

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


class Order(OrderFSMModel):
    customer = models.ForeignKey(to=get_user_model(), on_delete=models.PROTECT)
    delivery_address = models.ForeignKey(
        to=Address,
        on_delete=models.PROTECT, blank=True,
        null=True,
        related_name='order_deliveryaddress'
    )
    payment_address = models.ForeignKey(to=Address, on_delete=models.PROTECT,
                                        blank=True, null=True,
                                        related_name='order_paymentaddress')
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    currency = models.CharField(choices=CURRENCIES, default=EUR, max_length=3,
                                null=True, blank=True)
    rental_period = models.ForeignKey(to='chore.RentalPeriod', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.pk}: {self.customer.first_name} {self.customer.last_name} ({self.created_at})'


class OrderItem(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT,
                                related_name='order_items')
    order = models.ForeignKey(to=Order, on_delete=models.PROTECT,
                              related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.order.id} – {self.product.name} (x {self.quantity})'
