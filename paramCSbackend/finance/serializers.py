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

    def validate(self, data):
        """
        Check that the FromCurrencyID and ToCurrencyID are different.
        """
        if data['FromCurrencyID'] == data['ToCurrencyID']:
            raise serializers.ValidationError("FromCurrencyID and ToCurrencyID must be different")
        return data

class CurrencyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['CurrencyID', 'CurrencyName']

class CurrencyExchangeListSerializer(serializers.ModelSerializer):
    from_currency = serializers.CharField(source='FromCurrencyID.CurrencyID', read_only=True)
    to_currency = serializers.CharField(source='ToCurrencyID.CurrencyID', read_only=True)

    class Meta:
        model = CurrencyExchange
        fields = ['CurrencyExchangeID', 'from_currency', 'to_currency', 'ExchangeFactor', 'EffectiveDate']

class CurrencyExchangeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyExchange
        fields = ['FromCurrencyID', 'ToCurrencyID', 'ExchangeFactor', 'EffectiveDate']

    def validate(self, data):
        """
        Check that the FromCurrencyID and ToCurrencyID are different.
        """
        if data['FromCurrencyID'] == data['ToCurrencyID']:
            raise serializers.ValidationError("FromCurrencyID and ToCurrencyID must be different")
        return data
