from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Role, Rights, UserRights, CustomUser
from .serializers import RoleSerializer, RightsSerializer, UserRightsSerializer, CustomUserSerializer
from .permissions import IsAdminUser, IsSalesManager, IsSalesUser
import logging

logger = logging.getLogger(__name__)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        logger.info(f"Login attempt for user: {username}")
        
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            logger.info(f"Successful login for user: {username}")
        else:
            logger.warning(f"Failed login attempt for user: {username}")
            logger.warning(f"Response data: {response.data}")
        
        return response

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['RoleID', 'RoleName']
    search_fields = ['RoleName']
    ordering_fields = ['RoleName']

class RightsViewSet(viewsets.ModelViewSet):
    queryset = Rights.objects.all()
    serializer_class = RightsSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['RightsID', 'RightName']
    search_fields = ['RightName']
    ordering_fields = ['RightName']

class UserRightsViewSet(viewsets.ModelViewSet):
    queryset = UserRights.objects.all()
    serializer_class = UserRightsSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['UserRightsID', 'RoleID', 'RightsID']
    search_fields = ['UserRightsID']
    ordering_fields = ['UserRightsID']

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['username', 'email', 'is_active', 'RoleID']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined']

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'user activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'user deactivated'})
