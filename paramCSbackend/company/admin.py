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
    list_display = ('CompanyID', 'CompanyName', 'CountryID', 'sales_org_count')
    list_filter = ('CountryID',)
    search_fields = ('CompanyID', 'CompanyName')
    ordering = ('CompanyName',)

    def sales_org_count(self, obj):
        return obj.sales_organizations.count()
    sales_org_count.short_description = 'Sales Organizations'

@admin.register(SalesOrganization)
class SalesOrganizationAdmin(admin.ModelAdmin):
    list_display = ('SalesOrganizationID', 'SalesOrganizationName', 'CompanyID', 'account_group_count')
    list_filter = ('CompanyID',)
    search_fields = ('SalesOrganizationID', 'SalesOrganizationName')
    ordering = ('SalesOrganizationName',)

    def account_group_count(self, obj):
        return obj.account_groups.count()
    account_group_count.short_description = 'Account Groups'

@admin.register(AccountGroup)
class AccountGroupAdmin(admin.ModelAdmin):
    list_display = ('AccountGroupID', 'AccountGroupName', 'SalesOrganizationID')
    list_filter = ('SalesOrganizationID',)
    search_fields = ('AccountGroupID', 'AccountGroupName')
    ordering = ('AccountGroupName',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "SalesOrganizationID":
            kwargs["queryset"] = SalesOrganization.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
