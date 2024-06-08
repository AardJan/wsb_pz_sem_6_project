from django.test import TestCase
from unittest.mock import patch
from ..nbp_api import NBPAPI
from datetime import date


class NBPAPITests(TestCase):

    @patch("requests.get")
    def test_fetch_data_mock(self, mock_get):
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
        nbp_api = NBPAPI()
        data = nbp_api.fetch_data()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["currency"], "THB")
        self.assertEqual(data[0]["name"], "bat (Tajlandia)")
        self.assertEqual(data[1]["currency"], "USD")
        self.assertEqual(data[1]["name"], "dolar amerykański")

    def test_fetch_data_real(self):
        nbp_api = NBPAPI()
        data = nbp_api.fetch_data(start_date="2023-01-01", end_date="2023-01-10")
        self.assertTrue(len(data) > 0)
