from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from chore.factories import RentalPeriodFactory


class ViewsTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        RentalPeriodFactory()

    @parameterized.expand([
        ('rental-period-visualization-get_data',),
        ('rental-period-visualization',),
    ])
    def test_get_data(self, url):
        url = reverse(url)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
