from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Currency, CurrencyExchange
from .serializers import CurrencySerializer, CurrencyExchangeSerializer
from core.permissions import IsAdminUser, IsSalesManager, IsSalesUser

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['CurrencyID', 'CurrencyName']
    search_fields = ['CurrencyName']
    ordering_fields = ['CurrencyName']

class CurrencyExchangeViewSet(viewsets.ModelViewSet):
    queryset = CurrencyExchange.objects.all()
    serializer_class = CurrencyExchangeSerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['FromCurrencyID', 'ToCurrencyID', 'EffectiveDate']
    search_fields = ['CurrencyExchangeID']
    ordering_fields = ['EffectiveDate', 'ExchangeFactor']
