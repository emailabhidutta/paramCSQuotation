from django.contrib import admin
from .models import Currency, CurrencyExchange

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('CurrencyID', 'CurrencyName')
    search_fields = ('CurrencyID', 'CurrencyName')

@admin.register(CurrencyExchange)
class CurrencyExchangeAdmin(admin.ModelAdmin):
    list_display = ('CurrencyExchangeID', 'FromCurrencyID', 'ToCurrencyID', 'ExchangeFactor', 'EffectiveDate')
    list_filter = ('FromCurrencyID', 'ToCurrencyID', 'EffectiveDate')
    search_fields = ('CurrencyExchangeID',)
    date_hierarchy = 'EffectiveDate'
