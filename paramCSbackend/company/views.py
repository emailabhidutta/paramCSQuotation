from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Country, Company, SalesOrganization, AccountGroup
from .serializers import CountrySerializer, CompanySerializer, SalesOrganizationSerializer, AccountGroupSerializer
from core.permissions import IsAdminUser, IsSalesManager, IsSalesUser

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['CountryID', 'CountryName']
    search_fields = ['CountryName']
    ordering_fields = ['CountryName']

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['CompanyID', 'CountryID']
    search_fields = ['CompanyName']
    ordering_fields = ['CompanyName']

class SalesOrganizationViewSet(viewsets.ModelViewSet):
    queryset = SalesOrganization.objects.all()
    serializer_class = SalesOrganizationSerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['SalesOrganizationID', 'CompanyID']
    search_fields = ['SalesOrganizationName']
    ordering_fields = ['SalesOrganizationName']

class AccountGroupViewSet(viewsets.ModelViewSet):
    queryset = AccountGroup.objects.all()
    serializer_class = AccountGroupSerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['AccountGroupID', 'SalesOrganizationID']
    search_fields = ['AccountGroupName']
    ordering_fields = ['AccountGroupName']
