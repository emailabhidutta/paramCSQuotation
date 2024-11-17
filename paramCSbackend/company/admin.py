from django.contrib import admin
from django.utils.html import format_html
from .models import Country, Company, SalesOrganization, AccountGroup

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('CountryID', 'CountryName', 'CountryCode', 'company_count')
    search_fields = ('CountryID', 'CountryName', 'CountryCode')
    ordering = ('CountryName',)

    def company_count(self, obj):
        return obj.companies.count()
    company_count.short_description = 'Number of Companies'

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('CompanyID', 'CompanyName', 'CountryID', 'is_active_icon', 'sales_org_count')
    list_filter = ('CountryID', 'IsActive')
    search_fields = ('CompanyID', 'CompanyName')
    ordering = ('CompanyName',)
    actions = ['make_active', 'make_inactive']

    def is_active_icon(self, obj):
        if obj.IsActive:
            return format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        else:
            return format_html('<img src="/static/admin/img/icon-no.svg" alt="False">')
    is_active_icon.short_description = 'Active'

    def sales_org_count(self, obj):
        return obj.sales_organizations.count()
    sales_org_count.short_description = 'Sales Organizations'

    def make_active(self, request, queryset):
        queryset.update(IsActive=True)
    make_active.short_description = "Mark selected companies as active"

    def make_inactive(self, request, queryset):
        queryset.update(IsActive=False)
    make_inactive.short_description = "Mark selected companies as inactive"

@admin.register(SalesOrganization)
class SalesOrganizationAdmin(admin.ModelAdmin):
    list_display = ('SalesOrganizationID', 'SalesOrganizationName', 'CompanyID', 'is_active_icon', 'account_group_count')
    list_filter = ('CompanyID', 'IsActive')
    search_fields = ('SalesOrganizationID', 'SalesOrganizationName')
    ordering = ('SalesOrganizationName',)
    actions = ['make_active', 'make_inactive']

    def is_active_icon(self, obj):
        if obj.IsActive:
            return format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        else:
            return format_html('<img src="/static/admin/img/icon-no.svg" alt="False">')
    is_active_icon.short_description = 'Active'

    def account_group_count(self, obj):
        return obj.account_groups.count()
    account_group_count.short_description = 'Account Groups'

    def make_active(self, request, queryset):
        queryset.update(IsActive=True)
    make_active.short_description = "Mark selected sales organizations as active"

    def make_inactive(self, request, queryset):
        queryset.update(IsActive=False)
    make_inactive.short_description = "Mark selected sales organizations as inactive"

@admin.register(AccountGroup)
class AccountGroupAdmin(admin.ModelAdmin):
    list_display = ('AccountGroupID', 'AccountGroupName', 'SalesOrganizationID', 'is_active_icon')
    list_filter = ('SalesOrganizationID', 'IsActive')
    search_fields = ('AccountGroupID', 'AccountGroupName')
    ordering = ('AccountGroupName',)
    actions = ['make_active', 'make_inactive']

    def is_active_icon(self, obj):
        if obj.IsActive:
            return format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        else:
            return format_html('<img src="/static/admin/img/icon-no.svg" alt="False">')
    is_active_icon.short_description = 'Active'

    def make_active(self, request, queryset):
        queryset.update(IsActive=True)
    make_active.short_description = "Mark selected account groups as active"

    def make_inactive(self, request, queryset):
        queryset.update(IsActive=False)
    make_inactive.short_description = "Mark selected account groups as inactive"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "SalesOrganizationID":
            kwargs["queryset"] = SalesOrganization.objects.filter(IsActive=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
