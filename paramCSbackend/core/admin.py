from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Role, Rights, UserRights, CustomUser

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'RoleName', 'ParentRoleID')
    search_fields = ('RoleName',)
    list_filter = ('ParentRoleID',)

@admin.register(Rights)
class RightsAdmin(admin.ModelAdmin):
    list_display = ('RightsID', 'RightName')
    search_fields = ('RightsID', 'RightName')

@admin.register(UserRights)
class UserRightsAdmin(admin.ModelAdmin):
    list_display = ('UserRightsID', 'RoleID', 'RightsID')
    list_filter = ('RoleID', 'RightsID')
    search_fields = ('UserRightsID', 'RoleID__RoleName', 'RightsID__RightName')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'EmployeeNo', 'Department', 'RoleID')
    list_filter = ('is_staff', 'is_superuser', 'IsActive', 'RoleID', 'Department', 'is_deleted')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'EmployeeNo', 'PhoneNumber', 'Department')}),
        ('Permissions', {'fields': ('IsActive', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': ('RoleID', 'UserID', 'is_deleted', 'reset_password_token', 'reset_password_expires')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'EmployeeNo', 'PhoneNumber', 'Department', 'RoleID'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'EmployeeNo')
    ordering = ('username',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('UserID',)
        return self.readonly_fields
