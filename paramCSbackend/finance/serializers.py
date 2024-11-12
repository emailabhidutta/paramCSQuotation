from rest_framework import serializers
from .models import Currency, CurrencyExchange

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class CurrencyExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyExchange
        fields = '__all__'
