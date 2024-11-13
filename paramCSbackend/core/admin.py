from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role, Rights, UserRights

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'EmployeeNo', 'Department']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('EmployeeNo', 'IsActive', 'RoleID', 'PhoneNumber', 'Department', 'UserID', 'is_deleted', 'reset_password_token', 'reset_password_expires')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('EmployeeNo', 'IsActive', 'RoleID', 'PhoneNumber', 'Department', 'UserID')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(Rights)
admin.site.register(UserRights)
