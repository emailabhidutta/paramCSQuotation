from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import update_session_auth_hash
from .models import Role, Rights, UserRights, CustomUser
from .serializers import (
    RoleSerializer, RightsSerializer, UserRightsSerializer, 
    CustomUserSerializer, CustomUserListSerializer, CustomUserDetailSerializer,
    ChangePasswordSerializer, ResetPasswordSerializer, SetNewPasswordSerializer,
    LoginSerializer
)
from .permissions import IsAdminUser, IsSalesManager, IsSalesUser, IsAdminOrSalesManager, HasRightPermission
import logging
import uuid
from datetime import timedelta

logger = logging.getLogger(__name__)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        logger.info(f"Login attempt for user: {username}")
        
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            logger.info(f"Successful login for user: {username}")
        else:
            logger.warning(f"Failed login attempt for user: {username}")
        
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
    filterset_fields = ['username', 'email', 'IsActive', 'RoleID', 'Department']
    search_fields = ['username', 'email', 'Name', 'EmployeeNo']
    ordering_fields = ['username', 'date_joined', 'last_login']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action in ['me', 'change_password']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['reset_password', 'set_new_password']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminOrSalesManager]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return CustomUserListSerializer
        elif self.action in ['retrieve', 'me']:
            return CustomUserDetailSerializer
        return self.serializer_class

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.IsActive = '1'
        user.save()
        return Response({'status': 'user activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.IsActive = '0'
        user.save()
        return Response({'status': 'user deactivated'})

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if user.check_password(serializer.validated_data['old_password']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'status': 'password changed'})
            else:
                return Response({'error': 'incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                token = uuid.uuid4()
                user.reset_password_token = token
                user.reset_password_expires = timezone.now() + timedelta(hours=24)
                user.save()
                # Here you would send an email to the user with the reset link
                # The link would include the token
                return Response({'status': 'password reset email sent'})
            except CustomUser.DoesNotExist:
                return Response({'error': 'no user with this email'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def set_new_password(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                user = CustomUser.objects.get(reset_password_token=token)
                if user.reset_password_expires < timezone.now():
                    return Response({'error': 'token has expired'}, status=status.HTTP_400_BAD_REQUEST)
                user.set_password(new_password)
                user.reset_password_token = None
                user.reset_password_expires = None
                user.save()
                return Response({'status': 'password has been reset'})
            except CustomUser.DoesNotExist:
                return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[HasRightPermission])
    def users_by_role(self, request):
        role = request.query_params.get('role', None)
        if role is None:
            return Response({'error': 'role parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        users = CustomUser.objects.filter(RoleID__RoleName=role)
        serializer = CustomUserListSerializer(users, many=True)
        return Response(serializer.data)

    required_right = 'view_users_by_role'  # This is used by HasRightPermission
