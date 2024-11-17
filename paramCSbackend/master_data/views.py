from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import CustomerMaster, MaterialMaster, EmployeeMaster, EbauPriceList
from .serializers import (
    CustomerMasterSerializer, 
    MaterialMasterSerializer, 
    EmployeeMasterSerializer, 
    EbauPriceListSerializer,
    CustomerMasterListSerializer,
    MaterialMasterListSerializer,
    EmployeeMasterListSerializer,
    EbauPriceListListSerializer
)
from core.permissions import IsAdminUser, IsSalesManager, IsSalesUser

class CustomerMasterViewSet(viewsets.ModelViewSet):
    queryset = CustomerMaster.objects.all()
    serializer_class = CustomerMasterSerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['Customer', 'SalesOrganization', 'Country', 'CustomerClassification']
    search_fields = ['Customer', 'Name', 'Name2', 'SearchTerm']
    ordering_fields = ['Customer', 'Name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CustomerMasterListSerializer
        return CustomerMasterSerializer

class MaterialMasterViewSet(viewsets.ModelViewSet):
    queryset = MaterialMaster.objects.all()
    serializer_class = MaterialMasterSerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['Material', 'Plant', 'ProductGroup', 'ProductType']
    search_fields = ['Material', 'MaterialDescription', 'DrawingNo']
    ordering_fields = ['Material', 'MaterialDescription']

    def get_serializer_class(self):
        if self.action == 'list':
            return MaterialMasterListSerializer
        return MaterialMasterSerializer

class EmployeeMasterViewSet(viewsets.ModelViewSet):
    queryset = EmployeeMaster.objects.all()
    serializer_class = EmployeeMasterSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['EmployeeNo', 'CoCd', 'Status']
    search_fields = ['EmployeeNo', 'LastName', 'FirstName', 'OntrackID']
    ordering_fields = ['EmployeeNo', 'LastName']

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeMasterListSerializer
        return EmployeeMasterSerializer

class EbauPriceListViewSet(viewsets.ModelViewSet):
    queryset = EbauPriceList.objects.all()
    serializer_class = EbauPriceListSerializer
    permission_classes = [IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ConditionType', 'SalesOrganization', 'DistributionChannel', 'SalesGroup', 'Material', 'Customer']
    search_fields = ['Material', 'Customer']
    ordering_fields = ['ValidFrom', 'ValidTo', 'Rate']

    def get_serializer_class(self):
        if self.action == 'list':
            return EbauPriceListListSerializer
        return EbauPriceListSerializer
