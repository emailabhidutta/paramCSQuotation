from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Currency(models.Model):
    CurrencyID = models.CharField(max_length=4, primary_key=True)
    CurrencyName = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.CurrencyID} - {self.CurrencyName}"

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

class CurrencyExchange(models.Model):
    CurrencyExchangeID = models.CharField(max_length=4, primary_key=True)
    FromCurrencyID = models.ForeignKey(Currency, related_name='from_exchanges', on_delete=models.CASCADE)
    ToCurrencyID = models.ForeignKey(Currency, related_name='to_exchanges', on_delete=models.CASCADE)
    ExchangeFactor = models.DecimalField(
        max_digits=10, 
        decimal_places=4, 
        validators=[MinValueValidator(0.0001)]
    )
    EffectiveDate = models.DateField()

    def __str__(self):
        return f"{self.FromCurrencyID} to {self.ToCurrencyID}: {self.ExchangeFactor}"

    class Meta:
        verbose_name = "Currency Exchange Rate"
        verbose_name_plural = "Currency Exchange Rates"
        unique_together = ('FromCurrencyID', 'ToCurrencyID', 'EffectiveDate')

    def clean(self):
        if self.FromCurrencyID == self.ToCurrencyID:
            raise ValidationError("From and To currencies must be different.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
