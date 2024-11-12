from django.db import transaction
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import QuotationStatus, Quotation, QuotationDetails, QuotationItemDetails
from .serializers import (
    QuotationStatusSerializer, 
    QuotationSerializer, 
    QuotationDetailsSerializer, 
    QuotationItemDetailsSerializer
)
from core.permissions import IsAdminUser, IsSalesManager, IsSalesUser

class QuotationStatusViewSet(viewsets.ModelViewSet):
    queryset = QuotationStatus.objects.all()
    serializer_class = QuotationStatusSerializer
    permission_classes = [IsAdminUser]

class QuotationViewSet(viewsets.ModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['CustomerNumber', 'Date', 'QStatusID']
    search_fields = ['QuotationNo', 'CustomerNumber']
    ordering_fields = ['Date', 'CreationDate']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsSalesManager | IsAdminUser]
        else:
            permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
        return [permission() for permission in permission_classes]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quotation = serializer.save(created_by=request.user, last_modified_by=request.user)
        headers = self.get_success_headers(serializer.data)
        
        details_data = request.data.get('details', [])
        details_to_create = []
        items_to_create = []

        for detail in details_data:
            detail['QuoteId'] = quotation.QuoteId
            detail_serializer = QuotationDetailsSerializer(data=detail)
            detail_serializer.is_valid(raise_exception=True)
            details_to_create.append(QuotationDetails(**detail_serializer.validated_data))

        created_details = QuotationDetails.objects.bulk_create(details_to_create)

        for detail, created_detail in zip(details_data, created_details):
            items_data = detail.get('items', [])
            for item in items_data:
                item['QuotationDetailsId'] = created_detail.QuotationDetailsId
                item_serializer = QuotationItemDetailsSerializer(data=item)
                item_serializer.is_valid(raise_exception=True)
                items_to_create.append(QuotationItemDetails(**item_serializer.validated_data))

        QuotationItemDetails.objects.bulk_create(items_to_create)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        details_data = request.data.get('details', [])
        for detail in details_data:
            if 'QuotationDetailsId' in detail:
                detail_instance = QuotationDetails.objects.get(QuotationDetailsId=detail['QuotationDetailsId'])
                detail_serializer = QuotationDetailsSerializer(detail_instance, data=detail, partial=True)
            else:
                detail['QuoteId'] = instance.QuoteId
                detail_serializer = QuotationDetailsSerializer(data=detail)
            
            detail_serializer.is_valid(raise_exception=True)
            detail_instance = detail_serializer.save()

            items_data = detail.get('items', [])
            for item in items_data:
                if 'QuoteItemId' in item:
                    item_instance = QuotationItemDetails.objects.get(QuoteItemId=item['QuoteItemId'])
                    item_serializer = QuotationItemDetailsSerializer(item_instance, data=item, partial=True)
                else:
                    item['QuotationDetailsId'] = detail_instance.QuotationDetailsId
                    item_serializer = QuotationItemDetailsSerializer(data=item)
                
                item_serializer.is_valid(raise_exception=True)
                item_serializer.save()

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(last_modified_by=self.request.user)

class QuotationDetailsViewSet(viewsets.ModelViewSet):
    queryset = QuotationDetails.objects.all()
    serializer_class = QuotationDetailsSerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['QuoteId', 'SalesOrganization', 'SoldToCustomerNumber']
    search_fields = ['CustomerName', 'CustomerName2']
    ordering_fields = ['QuoteRevisionDate', 'QuoteValidFrom', 'QuoteValidUntil']

class QuotationItemDetailsViewSet(viewsets.ModelViewSet):
    queryset = QuotationItemDetails.objects.all()
    serializer_class = QuotationItemDetailsSerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['QuotationDetailsId', 'MaterialNumber']
    search_fields = ['MaterialDescription', 'CustomerMatNumber']
    ordering_fields = ['OrderQuantity', 'OrderValue']
