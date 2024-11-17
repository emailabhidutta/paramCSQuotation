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
    QuotationItemDetailsSerializer,
    QuotationListSerializer,
    QuotationSummarySerializer
)
from core.permissions import IsAdminUser, IsSalesManager, IsSalesUser
from .services import (
    create_quotation, update_quotation, submit_quotation, 
    approve_quotation, reject_quotation, cancel_quotation, 
    revise_quotation, delete_quotation_item,
    get_customer_details, get_item_rates, get_material_details
)
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
        
        recent_quotations = list(Quotation.objects.order_by('-CreationDate')[:5].values(
            'QuoteId', 'QuotationNo', 'CustomerNumber', 'CreationDate'
        ))
        
        total_value = QuotationItemDetails.objects.aggregate(total=Sum('OrderValue'))['total'] or 0

        summary_data = {
            'total_quotations': total_quotations,
            'quotation_status': quotation_status,
            'recent_quotations': recent_quotations,
            'total_value': total_value
        }
        
        serializer = QuotationSummarySerializer(summary_data)
        return Response(serializer.data)
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

    def get_serializer_class(self):
        if self.action == 'list':
            return QuotationListSerializer
        return QuotationSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsSalesManager | IsAdminUser]
        else:
            permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
        return [permission() for permission in permission_classes]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            quotation = create_quotation(request.data, request.user)
            serializer = self.get_serializer(quotation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'error': 'Validation error', 'details': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in create: {str(e)}")
            return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            updated_quotation = update_quotation(instance, request.data, request.user)
            serializer = self.get_serializer(updated_quotation)
            return Response(serializer.data)
        except serializers.ValidationError as e:
            return Response({'error': 'Validation error', 'details': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in update: {str(e)}")
            return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        quotation = self.get_object()
        try:
            submitted_quotation = submit_quotation(quotation, request.user)
            serializer = self.get_serializer(submitted_quotation)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        quotation = self.get_object()
        try:
            approved_quotation = approve_quotation(quotation, request.user)
            serializer = self.get_serializer(approved_quotation)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        quotation = self.get_object()
        reason = request.data.get('reason', '')
        try:
            rejected_quotation = reject_quotation(quotation, request.user, reason)
            serializer = self.get_serializer(rejected_quotation)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        quotation = self.get_object()
        try:
            cancelled_quotation = cancel_quotation(quotation, request.user)
            serializer = self.get_serializer(cancelled_quotation)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def revise(self, request, pk=None):
        quotation = self.get_object()
        try:
            revised_quotation = revise_quotation(quotation, request.user)
            serializer = self.get_serializer(revised_quotation)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def get_customer_details(self, request):
        search_term = request.query_params.get('search_term', '')
        try:
            customer_details = get_customer_details(search_term)
            return Response(customer_details)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def get_item_rates(self, request):
        customer_number = request.query_params.get('customer_number', '')
        material_number = request.query_params.get('material_number', '')
        sales_org = request.query_params.get('sales_org', '')
        distribution_channel = request.query_params.get('distribution_channel', '')
        try:
            item_rates = get_item_rates(customer_number, material_number, sales_org, distribution_channel)
            return Response(item_rates)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def get_material_details(self, request):
        material_number = request.query_params.get('material_number', '')
        try:
            material_details = get_material_details(material_number)
            return Response(material_details)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class QuotationDetailsViewSet(viewsets.ModelViewSet):
    queryset = QuotationDetails.objects.all()
    serializer_class = QuotationDetailsSerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['QuoteId', 'SalesOrganization', 'SoldToCustomerNumber']
    search_fields = ['CustomerName']
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
        try:
            delete_quotation_item(item.QuotationDetailsId.QuoteId, item.QuoteItemId)
            return Response({'status': 'item soft deleted'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
