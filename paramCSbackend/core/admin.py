from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import Role, Rights, UserRights, CustomUser, UserProfile, Department

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('RoleID', 'RoleName')
    search_fields = ('RoleName',)

@admin.register(Rights)
class RightsAdmin(admin.ModelAdmin):
    list_display = ('RightsID', 'RightName')
    search_fields = ('RightsID', 'RightName')

@admin.register(UserRights)
class UserRightsAdmin(admin.ModelAdmin):
    list_display = ('UserRightsID', 'RoleID', 'RightsID')
    list_filter = ('RoleID', 'RightsID')
    search_fields = ('UserRightsID', 'RoleID__RoleName', 'RightsID__RightName')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('Name', 'EmployeeNo', 'get_department', 'is_staff', 'RoleID', 'is_active')
    list_filter = ('IsActive', 'RoleID', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('Name', 'Password')}),
        ('Personal info', {'fields': ('EmployeeNo', 'RoleID')}),
        ('Permissions', {'fields': ('IsActive', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('Name', 'EmployeeNo', 'RoleID', 'Password', 'IsActive', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('Name', 'EmployeeNo')
    ordering = ('Name',)
    filter_horizontal = ('groups', 'user_permissions',)
    inlines = [UserProfileInline]

    def get_department(self, obj):
        return obj.profile.Department if hasattr(obj, 'profile') else None
    get_department.short_description = 'Department'

    def is_active(self, obj):
        return obj.IsActive == '1'
    is_active.boolean = True
    is_active.short_description = 'Is Active'

    def save_model(self, request, obj, form, change):
        if not change:
            # For new users, set the password
            obj.set_password(form.cleaned_data['Password'])
        elif 'Password' in form.changed_data:
            # If password is changed, hash it
            obj.set_password(form.cleaned_data['Password'])
        super().save_model(request, obj, form, change)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'PhoneNumber', 'Department', 'is_deleted')
    list_filter = ('Department', 'is_deleted')
    search_fields = ('user__Name', 'PhoneNumber')
    readonly_fields = ('user',)

# Unregister the Group model from admin.
# If you want to use Django's built-in permissions, you can remove this line.
admin.site.unregister(Group)
