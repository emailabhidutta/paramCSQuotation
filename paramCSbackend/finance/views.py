from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Currency, CurrencyExchange
from .serializers import (
    CurrencySerializer, 
    CurrencyExchangeSerializer, 
    CurrencyListSerializer,
    CurrencyExchangeListSerializer,
    CurrencyExchangeCreateUpdateSerializer
)
from core.permissions import IsAdminUser, IsSalesManager, IsSalesUser

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['CurrencyID', 'CurrencyName']
    search_fields = ['CurrencyName']
    ordering_fields = ['CurrencyName']

    def get_serializer_class(self):
        if self.action == 'list':
            return CurrencyListSerializer
        return CurrencySerializer

class CurrencyExchangeViewSet(viewsets.ModelViewSet):
    queryset = CurrencyExchange.objects.all()
    serializer_class = CurrencyExchangeSerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['FromCurrencyID', 'ToCurrencyID', 'EffectiveDate']
    search_fields = ['CurrencyExchangeID']
    ordering_fields = ['EffectiveDate', 'ExchangeFactor']

    def get_serializer_class(self):
        if self.action == 'list':
            return CurrencyExchangeListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CurrencyExchangeCreateUpdateSerializer
        return CurrencyExchangeSerializer

    @action(detail=False, methods=['get'])
    def latest_exchange_rates(self, request):
        latest_rates = CurrencyExchange.objects.order_by('FromCurrencyID', 'ToCurrencyID', '-EffectiveDate').distinct('FromCurrencyID', 'ToCurrencyID')
        serializer = CurrencyExchangeListSerializer(latest_rates, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_exchange_rate(self, request):
        from_currency = request.query_params.get('from')
        to_currency = request.query_params.get('to')
        date = request.query_params.get('date')

        if not all([from_currency, to_currency, date]):
            return Response({"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            exchange_rate = CurrencyExchange.objects.filter(
                FromCurrencyID=from_currency,
                ToCurrencyID=to_currency,
                EffectiveDate__lte=date
            ).order_by('-EffectiveDate').first()

            if exchange_rate:
                serializer = CurrencyExchangeSerializer(exchange_rate)
                return Response(serializer.data)
            else:
                return Response({"error": "Exchange rate not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
