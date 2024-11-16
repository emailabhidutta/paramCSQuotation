from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Role, Rights, UserRights, CustomUser

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'RoleName', 'RoleID')
    search_fields = ('RoleName',)

@admin.register(Rights)
class RightsAdmin(admin.ModelAdmin):
    list_display = ('RightsID', 'RightName')
    search_fields = ('RightsID', 'RightName')

@admin.register(UserRights)
class UserRightsAdmin(admin.ModelAdmin):
    list_display = ('UserRightsID', 'RoleID', 'RightsID')
    list_filter = ('RoleID', 'RightsID')
    search_fields = ('UserRightsID',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'EmployeeNo', 'Department')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'RoleID')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('EmployeeNo', 'IsActive', 'RoleID', 'PhoneNumber', 'Department', 'UserID', 'is_deleted')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('EmployeeNo', 'IsActive', 'RoleID', 'PhoneNumber', 'Department', 'UserID')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'EmployeeNo')
