from django.shortcuts import render
from rest_framework import viewsets
from .models import Country, Company, SalesOrganization, AccountGroup
from .serializers import CountrySerializer, CompanySerializer, SalesOrganizationSerializer, AccountGroupSerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class SalesOrganizationViewSet(viewsets.ModelViewSet):
    queryset = SalesOrganization.objects.all()
    serializer_class = SalesOrganizationSerializer

class AccountGroupViewSet(viewsets.ModelViewSet):
    queryset = AccountGroup.objects.all()
    serializer_class = AccountGroupSerializer