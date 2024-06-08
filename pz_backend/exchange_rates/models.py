from django.db import models


class ExchangeRate(models.Model):
    currency = models.CharField(max_length=3)
    name = models.CharField(max_length=100, default=None)
    exchange_date = models.DateField()
    rate = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ("currency", "exchange_date")
