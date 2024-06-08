import requests
from datetime import date, timedelta


class NBPAPI:
    BASE_URL = "http://api.nbp.pl/api/"

    def fetch_data(self, start_date=None, end_date=None, currency_code=None):
        if start_date is None:
            start_date = (date.today() - timedelta(days=90)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = date.today().strftime("%Y-%m-%d")

        if currency_code:
            url = f"{self.BASE_URL}/exchangerates/rates/a/{currency_code.lower()}/{start_date}/{end_date}"
        else:
            url = f"{self.BASE_URL}/exchangerates/tables/A/{start_date}/{end_date}"

        response = requests.get(url, headers={"Accept": "application/json"})
        response.raise_for_status()
        data = response.json()

        processed_data = []
        for table in data:
            for rate in table.get("rates", []):
                rate_info = {
                    "exchange_date": (
                        rate["effectiveDate"]
                        if currency_code
                        else table["effectiveDate"]
                    ),
                    "currency": table["code"] if currency_code else rate["code"],
                    "name": table["currency"] if currency_code else rate["currency"],
                    "rate": rate["mid"],
                }
                processed_data.append(rate_info)
        return processed_data
