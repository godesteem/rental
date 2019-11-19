from rest_framework import serializers

from chore.models import RentalPeriod
from chore.serializers import RentalPeriodSerializer
from shop.models import Address, Order, OrderItem, Product
from warehouse.models.warehouse import WarehouseItem


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    available_quantity = serializers.IntegerField(read_only=True)
    components = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'currency',
            'available_quantity',
            'status',
            'components',
        ]

    def get_components(self, obj):
        from warehouse.serializers.warehouse import \
            WarehouseItemComponentSerializer
        try:
            return WarehouseItemComponentSerializer(
                obj.warehouse_item.warehouse_components.all(), many=True
            ).data
        except WarehouseItem.DoesNotExist:
            return None


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', ]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    delivery_address = AddressSerializer()
    payment_address = AddressSerializer()
    rental_period = RentalPeriodSerializer(required=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'order_items', 'delivery_address',
            'payment_address', 'created_at', 'state',
            'price', 'currency', 'rental_period',
        ]

    def update_or_create_order_items(self, order_items, instance=None):
        if order_items is None:
            return

        if instance is None:
            instance = self.instance

        cleaned_order_items = []
        for order_item in order_items:
            cleaned_order_items.append({
                'quantity': order_item['quantity'],
                'product': Product.objects.get(
                    **order_item['product'])
            })

        for order_item in cleaned_order_items:
            order_item, _ = OrderItem.objects.update_or_create(
                order=instance, defaults=order_item)

    def update_or_create_address(self, address, address_type, instance=None):
        if address is None:
            return

        if instance is None:
            instance = self.instance

        address, _ = Address.objects.get_or_create(**address)
        setattr(instance, address_type, address)
        instance.save(update_fields=[address_type])

    def update_or_create_rental_period(self, rental_period, instance=None):
        if rental_period is None:
            return

        if instance is None:
            instance = self.instance

        rental_period, _ = RentalPeriod.objects.get_or_create(**rental_period)
        instance.rental_period = rental_period
        instance.save(update_fields=['rental_period'])

    def create(self, validated_data):
        order_items = validated_data.pop('order_items', None)
        delivery_address = validated_data.pop('delivery_address', None)
        payment_address = validated_data.pop('payment_address', None)
        rental_period = validated_data.pop('rental_period', None)

        instance = super().create(validated_data)

        self.update_or_create_order_items(order_items, instance)
        self.update_or_create_address(delivery_address, 'delivery_address',
                                      instance)
        self.update_or_create_address(payment_address, 'payment_address',
                                      instance)
        self.update_or_create_rental_period(rental_period, instance)
        return instance

    def update(self, instance, validated_data):
        order_items = validated_data.pop('order_items', None)
        delivery_address = validated_data.pop('delivery_address', None)
        payment_address = validated_data.pop('payment_address', None)
        rental_period = validated_data.pop('rental_period', None)

        self.update_or_create_order_items(order_items)
        self.update_or_create_address(delivery_address, 'delivery_address')
        self.update_or_create_address(payment_address, 'payment_address')
        self.update_or_create_rental_period(rental_period)
        return super().update(instance, validated_data)
