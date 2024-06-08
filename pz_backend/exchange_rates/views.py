from datetime import date, timedelta

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from .nbp_api import NBPAPI


class ExchangeRateListView(ListAPIView):
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = date.today()
        week_ago = today - timedelta(days=6)
        return ExchangeRate.objects.filter(exchange_date__range=[week_ago, today])


class ExchangeRateDetailView(ListAPIView):
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        currency = self.kwargs["currency_code"]
        return ExchangeRate.objects.filter(currency=currency).order_by(
            "-exchange_date"
        )[:7]


class ExchangeRateYearView(ListAPIView):
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        currency = self.kwargs["currency_code"]
        year = self.kwargs["year"]
        return ExchangeRate.objects.filter(currency=currency, exchange_date__year=year)


class ExchangeRateMonthView(ListAPIView):
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        currency = self.kwargs["currency_code"]
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        return ExchangeRate.objects.filter(
            currency=currency, exchange_date__year=year, exchange_date__month=month
        )


class ExchangeRateDayView(ListAPIView):
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        currency = self.kwargs["currency_code"]
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]
        return ExchangeRate.objects.filter(
            currency=currency,
            exchange_date__year=year,
            exchange_date__month=month,
            exchange_date__day=day,
        )


class FetchExchangeRatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        currency = self.kwargs.get("currency_code", None)
        start_date = request.query_params.get("start_date", None)
        end_date = request.query_params.get("end_date", None)

        nbp_api = NBPAPI()
        data = nbp_api.fetch_data(
            start_date=start_date, end_date=end_date, currency_code=currency
        )

        return Response(data)
