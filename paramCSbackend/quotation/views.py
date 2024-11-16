from django.db import connection, transaction
from django.db.utils import OperationalError, ProgrammingError
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import status, viewsets, filters, serializers
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncDate
from .models import QuotationStatus, Quotation, QuotationDetails, QuotationItemDetails
from .serializers import (
    QuotationStatusSerializer, 
    QuotationSerializer, 
    QuotationDetailsSerializer, 
    QuotationItemDetailsSerializer
)
from core.permissions import IsAdminUser, IsSalesManager, IsSalesUser
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsSalesUser | IsSalesManager | IsAdminUser])
def dashboard_view(request):
    try:
        total_quotations = Quotation.objects.count()
        
        quotation_status = list(Quotation.objects.values('QStatusID__QStatusName')
                                .annotate(count=Count('QuoteId'))
                                .order_by('QStatusID__QStatusName'))
        
        recent_quotations = list(Quotation.objects.annotate(
            creation_date=TruncDate('CreationDate')
        ).order_by('-CreationDate')[:5].values(
            'QuoteId', 'QuotationNo', 'CustomerNumber', 'creation_date'
        ))
        
        total_value = QuotationItemDetails.objects.aggregate(total=Sum('OrderValue'))['total'] or 0

        return Response({
            'total_quotations': total_quotations,
            'quotation_status': quotation_status,
            'recent_quotations': recent_quotations,
            'total_value': total_value
        })
    except Exception as e:
        logger.error(f"Unexpected error in dashboard_view: {str(e)}")
        return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QuotationStatusViewSet(viewsets.ModelViewSet):
    queryset = QuotationStatus.objects.all()
    serializer_class = QuotationStatusSerializer
    permission_classes = [IsAdminUser]

class QuotationViewSet(viewsets.ModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['CustomerNumber', 'CreationDate', 'QStatusID']
    search_fields = ['QuotationNo', 'CustomerNumber']
    ordering_fields = ['CreationDate', 'QuotationNo']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsSalesManager | IsAdminUser]
        else:
            permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
        return [permission() for permission in permission_classes]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
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
        except serializers.ValidationError as e:
            return Response({'error': 'Validation error', 'details': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in create: {str(e)}")
            return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
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
        except serializers.ValidationError as e:
            return Response({'error': 'Validation error', 'details': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in update: {str(e)}")
            return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_update(self, serializer):
        serializer.save(last_modified_by=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        quotation = self.get_object()
        try:
            quotation.approve(request.user)
            return Response({'status': 'quotation approved'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        quotation = self.get_object()
        reason = request.data.get('reason', '')
        try:
            quotation.reject(request.user, reason)
            return Response({'status': 'quotation rejected'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def revise(self, request, pk=None):
        quotation = self.get_object()
        try:
            quotation.revise(request.user)
            return Response({'status': 'quotation revised'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class QuotationDetailsViewSet(viewsets.ModelViewSet):
    queryset = QuotationDetails.objects.all()
    serializer_class = QuotationDetailsSerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['QuoteId', 'SalesOrganization', 'Customer']
    search_fields = ['Customer']
    ordering_fields = ['QuoteRevisionDate']

class QuotationItemDetailsViewSet(viewsets.ModelViewSet):
    queryset = QuotationItemDetails.objects.all()
    serializer_class = QuotationItemDetailsSerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['QuotationDetailsId', 'MaterialNumber']
    search_fields = ['MaterialDescription', 'CustomerMatNumber']
    ordering_fields = ['OrderQuantity', 'OrderValue']

    @action(detail=True, methods=['post'])
    def soft_delete(self, request, pk=None):
        item = self.get_object()
        item.IsDeleted = True
        item.save()
        return Response({'status': 'item soft deleted'})
