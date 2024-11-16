from django.contrib import admin
from .models import Country, Company, SalesOrganization, AccountGroup

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('CountryID', 'CountryName')
    search_fields = ('CountryID', 'CountryName')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('CompanyID', 'CompanyName', 'CountryID')
    list_filter = ('CountryID',)
    search_fields = ('CompanyID', 'CompanyName')

@admin.register(SalesOrganization)
class SalesOrganizationAdmin(admin.ModelAdmin):
    list_display = ('SalesOrganizationID', 'SalesOrganizationName', 'CompanyID')
    list_filter = ('CompanyID',)
    search_fields = ('SalesOrganizationID', 'SalesOrganizationName')

@admin.register(AccountGroup)
class AccountGroupAdmin(admin.ModelAdmin):
    list_display = ('AccountGroupID', 'AccountGroupName', 'SalesOrganizationID')
    list_filter = ('SalesOrganizationID',)
    search_fields = ('AccountGroupID', 'AccountGroupName')
