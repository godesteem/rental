from django_fsm import FSMField, transition


class OrderFSMMixin:
    NEW = 'new'
    ACCEPTED = 'accepted'
    IN_DELIVERY = 'in-delivery'
    AT_CUSTOMER = 'at-customer'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'
    STATES = [
        (NEW, 'New'),
        (ACCEPTED, 'Accepted'),
        (IN_DELIVERY, 'In delivery'),
        (AT_CUSTOMER, 'At customer'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]

    state = FSMField(default=NEW, protected=True, choices=STATES)
    @transition(field=state, source=NEW, target=ACCEPTED)
    def accept(self):
        pass

    @transition(field=state, source=ACCEPTED, target=IN_DELIVERY)
    def start_delivery(self):
        pass

    @transition(field=state, source=IN_DELIVERY, target=AT_CUSTOMER)
    def arrive_at_customer(self):
        pass

    @transition(field=state, source=AT_CUSTOMER, target=DELIVERED)
    def deliver(self):
        pass

    @transition(field=state, source=[NEW, ACCEPTED, IN_DELIVERY, AT_CUSTOMER], target=CANCELED)
    def cancel(self):
        pass

