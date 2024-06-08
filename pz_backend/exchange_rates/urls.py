from django.urls import path
from .views import (
    ExchangeRateListView,
    ExchangeRateDetailView,
    ExchangeRateYearView,
    ExchangeRateMonthView,
    ExchangeRateDayView,
)

urlpatterns = [
    path(
        "exchange-rates/",
        ExchangeRateListView.as_view(),
        name="exchange-rate-list",
    ),
    path(
        "exchange-rates/<str:currency_code>/",
        ExchangeRateDetailView.as_view(),
        name="exchange-rate-detail",
    ),
    path(
        "exchange-rates/<str:currency_code>/year/<int:year>/",
        ExchangeRateYearView.as_view(),
        name="exchange-rate-year",
    ),
    path(
        "exchange-rates/<str:currency_code>/year/<int:year>/month/<int:month>/",
        ExchangeRateMonthView.as_view(),
        name="exchange-rate-month",
    ),
    path(
        "exchange-rates/<str:currency_code>/year/<int:year>/month/<int:month>/day/<int:day>/",
        ExchangeRateDayView.as_view(),
        name="exchange-rate-day",
    ),
]
