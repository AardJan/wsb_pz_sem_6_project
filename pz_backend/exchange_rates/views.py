from rest_framework import generics
from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from datetime import date, timedelta
from rest_framework.permissions import IsAuthenticated


class ExchangeRateListView(generics.ListAPIView):
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = date.today()
        week_ago = today - timedelta(days=6)
        return ExchangeRate.objects.filter(date__range=[week_ago, today])


class ExchangeRateDetailView(generics.ListAPIView):
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        currency = self.kwargs["currency_code"]
        return ExchangeRate.objects.filter(currency=currency).order_by("-date")[:7]


class ExchangeRateYearView(generics.ListAPIView):
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        currency = self.kwargs["currency_code"]
        year = self.kwargs["year"]
        return ExchangeRate.objects.filter(currency=currency, date__year=year)


class ExchangeRateMonthView(generics.ListAPIView):
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        currency = self.kwargs["currency_code"]
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        return ExchangeRate.objects.filter(
            currency=currency, date__year=year, date__month=month
        )


class ExchangeRateDayView(generics.ListAPIView):
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        currency = self.kwargs["currency_code"]
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]
        return ExchangeRate.objects.filter(
            currency=currency, date__year=year, date__month=month, date__day=day
        )
