from rest_framework import serializers
from .models import Currency, CurrencyExchange

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class CurrencyExchangeSerializer(serializers.ModelSerializer):
    from_currency_name = serializers.CharField(source='FromCurrencyID.CurrencyName', read_only=True)
    to_currency_name = serializers.CharField(source='ToCurrencyID.CurrencyName', read_only=True)

    class Meta:
        model = CurrencyExchange
        fields = '__all__'