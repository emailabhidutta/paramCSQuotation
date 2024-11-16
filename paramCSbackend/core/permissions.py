import logging
from rest_framework import permissions

logger = logging.getLogger(__name__)

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class IsSalesManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.RoleID is not None and request.user.RoleID.RoleName == 'Sales Manager'
        except AttributeError as e:
            logger.error(f"Error checking IsSalesManager permission: {str(e)}")
            return False

class IsSalesUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.RoleID is not None and request.user.RoleID.RoleName == 'Sales User'
        except AttributeError as e:
            logger.error(f"Error checking IsSalesUser permission: {str(e)}")
            return False

class IsAdminOrSalesManagerOrSalesUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        try:
            return request.user.RoleID is not None and request.user.RoleID.RoleName in ['Sales Manager', 'Sales User']
        except AttributeError as e:
            logger.error(f"Error checking IsAdminOrSalesManagerOrSalesUser permission: {str(e)}")
            return False

class IsAdminOrSalesManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        try:
            return request.user.RoleID is not None and request.user.RoleID.RoleName == 'Sales Manager'
        except AttributeError as e:
            logger.error(f"Error checking IsAdminOrSalesManager permission: {str(e)}")
            return False
