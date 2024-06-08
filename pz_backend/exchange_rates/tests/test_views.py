from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from ..models import ExchangeRate
from datetime import date, timedelta
from unittest.mock import patch

User = get_user_model()


class ExchangeRateTests(APITestCase):
    def setUp(self):
        today = date.today()
        for i in range(10):
            ExchangeRate.objects.create(
                currency="USD",
                name="dolar amerykański",
                exchange_date=today - timedelta(days=i),
                rate=3.75 + i * 0.01,
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
                item["currency"] == "USD" and item["exchange_date"].startswith("2023")
                for item in response.data
            )
        )

    def test_get_exchange_rate_by_month(self):
        url = reverse("exchange-rate-month", args=["USD", 2023, 6])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            all(
                item["currency"] == "USD"
                and item["exchange_date"].startswith("2023-06")
                for item in response.data
            )
        )

    def test_get_exchange_rate_by_day(self):
        url = reverse("exchange-rate-day", args=["USD", 2023, 6, 8])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            all(
                item["currency"] == "USD" and item["exchange_date"] == "2023-06-08"
                for item in response.data
            )
        )

    @patch("requests.get")
    def test_fetch_exchange_rates_mock(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "table": "A",
                "no": "110/A/NBP/2024",
                "effectiveDate": "2024-06-07",
                "rates": [
                    {"currency": "bat (Tajlandia)", "code": "THB", "mid": 0.1080},
                    {"currency": "dolar amerykański", "code": "USD", "mid": 3.9389},
                ],
            }
        ]

        url = reverse("fetch-exchange-rates")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["currency"], "THB")
        self.assertEqual(response.data[0]["name"], "bat (Tajlandia)")
        self.assertEqual(response.data[1]["currency"], "USD")
        self.assertEqual(response.data[1]["name"], "dolar amerykański")

    def test_fetch_exchange_rates_real(self):
        url = reverse("fetch-exchange-rates")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("currency" in response.data[0])
