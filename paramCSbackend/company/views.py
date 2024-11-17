from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Country, Company, SalesOrganization, AccountGroup
from .serializers import (
    CountrySerializer, CountryDetailSerializer,
    CompanySerializer, CompanyDetailSerializer,
    SalesOrganizationSerializer, SalesOrganizationDetailSerializer,
    AccountGroupSerializer
)
from core.permissions import IsAdminUser, IsSalesManager, IsSalesUser

class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsSalesManager | IsAdminUser]
        else:
            permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
        return [permission() for permission in permission_classes]

class CountryViewSet(BaseViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filterset_fields = ['CountryID', 'CountryName', 'CountryCode']
    search_fields = ['CountryName', 'CountryCode']
    ordering_fields = ['CountryName', 'CountryCode']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CountryDetailSerializer
        return CountrySerializer

    @action(detail=False, methods=['get'])
    def active_countries(self, request):
        active_countries = self.get_queryset().filter(companies__IsActive=True).distinct()
        serializer = self.get_serializer(active_countries, many=True)
        return Response(serializer.data)

class CompanyViewSet(BaseViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_fields = ['CompanyID', 'CountryID', 'IsActive']
    search_fields = ['CompanyName']
    ordering_fields = ['CompanyName', 'created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompanyDetailSerializer
        return CompanySerializer

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        company = self.get_object()
        company.IsActive = not company.IsActive
        company.save()
        return Response({'status': 'company active status updated'})

class SalesOrganizationViewSet(BaseViewSet):
    queryset = SalesOrganization.objects.all()
    serializer_class = SalesOrganizationSerializer
    filterset_fields = ['SalesOrganizationID', 'CompanyID', 'IsActive']
    search_fields = ['SalesOrganizationName']
    ordering_fields = ['SalesOrganizationName', 'created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SalesOrganizationDetailSerializer
        return SalesOrganizationSerializer

    @action(detail=False, methods=['get'])
    def by_company(self, request):
        company_id = request.query_params.get('company_id', None)
        if company_id is None:
            return Response({'error': 'company_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        sales_orgs = self.get_queryset().filter(CompanyID=company_id)
        serializer = self.get_serializer(sales_orgs, many=True)
        return Response(serializer.data)

class AccountGroupViewSet(BaseViewSet):
    queryset = AccountGroup.objects.all()
    serializer_class = AccountGroupSerializer
    filterset_fields = ['AccountGroupID', 'SalesOrganizationID', 'IsActive']
    search_fields = ['AccountGroupName']
    ordering_fields = ['AccountGroupName', 'created_at']

    @action(detail=False, methods=['get'])
    def by_sales_org(self, request):
        sales_org_id = request.query_params.get('sales_org_id', None)
        if sales_org_id is None:
            return Response({'error': 'sales_org_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        account_groups = self.get_queryset().filter(SalesOrganizationID=sales_org_id)
        serializer = self.get_serializer(account_groups, many=True)
        return Response(serializer.data)
