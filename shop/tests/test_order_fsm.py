from django.test import TestCase

from shop.factories.order import OrderFactory


class OrderFSMTestCase(TestCase):
    def setUp(self) -> None:
        self.order = OrderFactory()

    def test_allowed_transitions(self):
        self.order.accept()
        self.order.start_delivery()
        self.order.arrive_at_customer()
        self.order.deliver()

    def test_cancellation_from_state(self):
        self.order.cancel()
