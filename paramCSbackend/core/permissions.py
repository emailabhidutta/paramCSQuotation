from django.contrib.auth.models import User
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class IsSalesManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.customuser.RoleID.RoleName == 'Sales Manager'
        except AttributeError:
            return False

class IsSalesUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.customuser.RoleID.RoleName == 'Sales User'
        except AttributeError:
            return False

class IsAdminOrSalesManagerOrSalesUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        try:
            role_name = request.user.customuser.RoleID.RoleName
            return role_name in ['Sales Manager', 'Sales User']
        except AttributeError:
            return False

class IsAdminOrSalesManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        try:
            return request.user.customuser.RoleID.RoleName == 'Sales Manager'
        except AttributeError:
            return False
