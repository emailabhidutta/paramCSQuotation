from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import Country, Company, SalesOrganization, AccountGroup
from .serializers import (
    CountrySerializer, CountryDetailSerializer, CountryListSerializer,
    CompanySerializer, CompanyDetailSerializer, CompanyListSerializer,
    SalesOrganizationSerializer, SalesOrganizationDetailSerializer, SalesOrganizationListSerializer,
    AccountGroupSerializer, AccountGroupListSerializer
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
        if self.action == 'list':
            return CountryListSerializer
        elif self.action == 'retrieve':
            return CountryDetailSerializer
        return CountrySerializer

    @action(detail=False, methods=['get'])
    def active_countries(self, request):
        active_countries = self.get_queryset().filter(companies__isnull=False).distinct()
        serializer = self.get_serializer(active_countries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def countries_with_stats(self, request):
        countries = self.get_queryset().annotate(
            company_count=Count('companies', distinct=True),
            sales_org_count=Count('companies__sales_organizations', distinct=True)
        )
        serializer = CountryListSerializer(countries, many=True)
        return Response(serializer.data)

class CompanyViewSet(BaseViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_fields = ['CompanyID', 'CountryID']
    search_fields = ['CompanyName']
    ordering_fields = ['CompanyName']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompanyListSerializer
        elif self.action == 'retrieve':
            return CompanyDetailSerializer
        return CompanySerializer

    @action(detail=False, methods=['get'])
    def companies_by_country(self, request):
        country_id = request.query_params.get('country_id')
        if not country_id:
            return Response({"error": "country_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        companies = self.get_queryset().filter(CountryID=country_id)
        serializer = CompanyListSerializer(companies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def company_structure(self, request, pk=None):
        company = self.get_object()
        sales_orgs = company.sales_organizations.all()
        data = {
            "company": CompanySerializer(company).data,
            "sales_organizations": SalesOrganizationListSerializer(sales_orgs, many=True).data
        }
        return Response(data)

class SalesOrganizationViewSet(BaseViewSet):
    queryset = SalesOrganization.objects.all()
    serializer_class = SalesOrganizationSerializer
    filterset_fields = ['SalesOrganizationID', 'CompanyID']
    search_fields = ['SalesOrganizationName']
    ordering_fields = ['SalesOrganizationName']

    def get_serializer_class(self):
        if self.action == 'list':
            return SalesOrganizationListSerializer
        elif self.action == 'retrieve':
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

    @action(detail=True, methods=['get'])
    def sales_org_details(self, request, pk=None):
        sales_org = self.get_object()
        account_groups = sales_org.account_groups.all()
        data = {
            "sales_organization": SalesOrganizationSerializer(sales_org).data,
            "account_groups": AccountGroupListSerializer(account_groups, many=True).data
        }
        return Response(data)

class AccountGroupViewSet(BaseViewSet):
    queryset = AccountGroup.objects.all()
    serializer_class = AccountGroupSerializer
    filterset_fields = ['AccountGroupID', 'SalesOrganizationID']
    search_fields = ['AccountGroupName']
    ordering_fields = ['AccountGroupName']

    def get_serializer_class(self):
        if self.action == 'list':
            return AccountGroupListSerializer
        return AccountGroupSerializer

    @action(detail=False, methods=['get'])
    def by_sales_org(self, request):
        sales_org_id = request.query_params.get('sales_org_id', None)
        if sales_org_id is None:
            return Response({'error': 'sales_org_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        account_groups = self.get_queryset().filter(SalesOrganizationID=sales_org_id)
        serializer = self.get_serializer(account_groups, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def account_groups_with_stats(self, request):
        account_groups = self.get_queryset().annotate(
            customer_count=Count('customermaster', distinct=True)
        )
        serializer = AccountGroupListSerializer(account_groups, many=True)
        return Response(serializer.data)
