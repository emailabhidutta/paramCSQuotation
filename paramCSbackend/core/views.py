from django.shortcuts import render
from rest_framework import viewsets
from .models import Role, Rights, UserRights, CustomUser
from .serializers import RoleSerializer, RightsSerializer, UserRightsSerializer, CustomUserSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RightsViewSet(viewsets.ModelViewSet):
    queryset = Rights.objects.all()
    serializer_class = RightsSerializer

class UserRightsViewSet(viewsets.ModelViewSet):
    queryset = UserRights.objects.all()
    serializer_class = UserRightsSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer