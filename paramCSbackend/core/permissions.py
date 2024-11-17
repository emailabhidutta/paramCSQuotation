import logging
from rest_framework import permissions

logger = logging.getLogger(__name__)

class BaseRolePermission(permissions.BasePermission):
    def has_role(self, user, role_name):
        if not user.is_authenticated:
            return False
        try:
            return user.has_role(role_name)
        except AttributeError as e:
            logger.error(f"Error checking {self.__class__.__name__} permission: {str(e)}")
            return False

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class IsSalesManager(BaseRolePermission):
    def has_permission(self, request, view):
        return self.has_role(request.user, 'Sales Manager')

class IsSalesUser(BaseRolePermission):
    def has_permission(self, request, view):
        return self.has_role(request.user, 'Sales User')

class IsAdminOrSalesManagerOrSalesUser(BaseRolePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        return self.has_role(request.user, 'Sales Manager') or self.has_role(request.user, 'Sales User')

class IsAdminOrSalesManager(BaseRolePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        return self.has_role(request.user, 'Sales Manager')

class HasRightPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        required_right = getattr(view, 'required_right', None)
        if required_right is None:
            return False
        try:
            return request.user.has_right(required_right)
        except AttributeError as e:
            logger.error(f"Error checking HasRightPermission: {str(e)}")
            return False

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
