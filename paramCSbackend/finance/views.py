from django.shortcuts import render
from rest_framework import viewsets
from .models import Currency, CurrencyExchange
from .serializers import CurrencySerializer, CurrencyExchangeSerializer

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class CurrencyExchangeViewSet(viewsets.ModelViewSet):
    queryset = CurrencyExchange.objects.all()
    serializer_class = CurrencyExchangeSerializer