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
        ('management',),
    ])
    def test_get_data(self, url):
        url = reverse(url)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @parameterized.expand([
        ({'view': 'orders,products,rental-periods'},),
        ({},),
    ])
    def test_visualization(self, kwargs):
        url = reverse('visualization')

        response = self.client.get(url, data=kwargs)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
