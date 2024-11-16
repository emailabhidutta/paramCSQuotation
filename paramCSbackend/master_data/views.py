from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import CustomerMaster, MaterialMaster
from .serializers import CustomerMasterSerializer, MaterialMasterSerializer
from core.permissions import IsAdminUser, IsSalesManager, IsSalesUser

class CustomerMasterViewSet(viewsets.ModelViewSet):
    queryset = CustomerMaster.objects.all()
    serializer_class = CustomerMasterSerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['CustomerNumber', 'SalesOrg', 'Country', 'CustomerClass']
    search_fields = ['CustomerNumber', 'CustomerName1', 'CustomerName2', 'SearchTerm']
    ordering_fields = ['CustomerNumber', 'CustomerName1']

class MaterialMasterViewSet(viewsets.ModelViewSet):
    queryset = MaterialMaster.objects.all()
    serializer_class = MaterialMasterSerializer
    permission_classes = [IsSalesUser | IsSalesManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['MaterialNumber', 'Plant', 'ProductGroup', 'ProductType']
    search_fields = ['MaterialNumber', 'MaterialDescription', 'DrawingNumber']
    ordering_fields = ['MaterialNumber', 'MaterialDescription']
