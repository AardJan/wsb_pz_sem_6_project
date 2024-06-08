from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import ExchangeRate
from datetime import date, timedelta


User = get_user_model()


class ExchangeRateTests(APITestCase):
    def setUp(self):
        today = date.today()
        for i in range(10):
            ExchangeRate.objects.create(
                currency="USD", date=today - timedelta(days=i), rate=3.75 + i * 0.01
            )

        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_get_all_exchange_rates(self):
        url = reverse("exchange-rate-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)

    def test_get_exchange_rate_by_currency(self):
        url = reverse("exchange-rate-detail", args=["USD"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["currency"], "USD")

    def test_get_exchange_rate_by_year(self):
        url = reverse("exchange-rate-year", args=["USD", 2023])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            all(
                item["currency"] == "USD" and item["date"].startswith("2023")
                for item in response.data
            )
        )

    def test_get_exchange_rate_by_month(self):
        url = reverse("exchange-rate-month", args=["USD", 2023, 6])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            all(
                item["currency"] == "USD" and item["date"].startswith("2023-06")
                for item in response.data
            )
        )

    def test_get_exchange_rate_by_day(self):
        url = reverse("exchange-rate-day", args=["USD", 2023, 6, 8])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            all(
                item["currency"] == "USD" and item["date"] == "2023-06-08"
                for item in response.data
            )
        )
