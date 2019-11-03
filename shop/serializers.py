from rest_framework import serializers

from shop.models import Address, Order, OrderItem, Product


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'currency', ]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', ]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    delivery_address = AddressSerializer()
    payment_address = AddressSerializer()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_items', 'delivery_address',
                  'payment_address', 'created_at', 'state',
                  'price', 'currency']

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

    def update_or_create_delivery_address(self, delivery_address,
                                          instance=None):
        if delivery_address is None:
            return

        if instance is None:
            instance = self.instance

        address, _ = Address.objects.get_or_create(**delivery_address)
        instance.delivery_address = address
        instance.save(update_fields=['delivery_address'])

    def update_or_create_payment_address(self, payment_address,
                                         instance=None):
        if payment_address is None:
            return

        if instance is None:
            instance = self.instance

        address, _ = Address.objects.get_or_create(**payment_address)
        instance.payment_address = address
        instance.save(update_fields=['payment_address'])

    def create(self, validated_data):
        order_items = validated_data.pop('order_items', None)
        delivery_address = validated_data.pop('delivery_address', None)
        payment_address = validated_data.pop('payment_address', None)

        instance = super().create(validated_data)

        self.update_or_create_order_items(order_items, instance)
        self.update_or_create_delivery_address(delivery_address, instance)
        self.update_or_create_payment_address(payment_address, instance)
        return instance

    def update(self, instance, validated_data):
        order_items = validated_data.pop('order_items', None)
        delivery_address = validated_data.pop('delivery_address', None)
        payment_address = validated_data.pop('payment_address', None)

        self.update_or_create_order_items(order_items)
        self.update_or_create_delivery_address(delivery_address)
        self.update_or_create_payment_address(payment_address)
        return super().update(instance, validated_data)
