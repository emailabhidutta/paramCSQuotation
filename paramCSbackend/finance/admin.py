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

    def save_model(self, request, obj, form, change):
        if not obj.ExchangeFactor:
            obj.ExchangeFactor = 1  # Set default value if not provided
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["FromCurrencyID", "ToCurrencyID"]:
            kwargs["queryset"] = Currency.objects.order_by('CurrencyID')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['ExchangeFactor'].initial = 1  # Set default value in the form
        return form
