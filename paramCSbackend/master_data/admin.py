from django.contrib import admin
from .models import CustomerMaster, MaterialMaster, EmployeeMaster, EbauPriceList

@admin.register(CustomerMaster)
class CustomerMasterAdmin(admin.ModelAdmin):
    list_display = ('Customer', 'Name', 'SalesOrganization', 'City', 'Country')
    list_filter = ('SalesOrganization', 'Country', 'CustomerClassification')
    search_fields = ('Customer', 'Name', 'Name2', 'SearchTerm')
    fieldsets = (
        ('Basic Info', {
            'fields': ('Customer', 'Name', 'Name2', 'SearchTerm')
        }),
        ('Organization', {
            'fields': ('SalesOrganization', 'AccountGroup', 'CustomerClassification', 'SalesGroup')
        }),
        ('Address', {
            'fields': ('Street', 'City', 'Country')
        }),
        ('Business Terms', {
            'fields': ('CustPriceProcedure', 'TermsOfPayment', 'Incoterms', 'IncotermsPart2', 'Currency')
        }),
        ('Status', {
            'fields': ('OrderBlockForSalesArea', 'CentralDelBlock', 'Status')
        }),
        ('System Fields', {
            'fields': ('CreatedOn', 'CreatedSource', 'LastUpdate', 'UpdatedSource')
        }),
    )

@admin.register(MaterialMaster)
class MaterialMasterAdmin(admin.ModelAdmin):
    list_display = ('Material', 'MaterialDescription', 'Plant', 'ProductGroup', 'BaseUnitOfMeasure')
    list_filter = ('Plant', 'ProductGroup', 'ProductType', 'Lifecycle')
    search_fields = ('Material', 'MaterialDescription', 'DrawingNo')
    fieldsets = (
        ('Basic Info', {
            'fields': ('Material', 'MaterialDescription', 'Plant', 'XPlantMatlStatus')
        }),
        ('Details', {
            'fields': ('DrawingNo', 'Description', 'DescriptionText', 'BasicMaterial', 'BasicMaterialDesc')
        }),
        ('Classification', {
            'fields': ('MachineType', 'ProductGroup', 'ProductType', 'Lifecycle', 'ProductHierarchy')
        }),
        ('Other', {
            'fields': ('OldMaterialNumber', 'BaseUnitOfMeasure')
        }),
        ('System Fields', {
            'fields': ('Status', 'CreatedOn', 'CreatedSource', 'LastUpdate', 'UpdatedSource')
        }),
    )

@admin.register(EmployeeMaster)
class EmployeeMasterAdmin(admin.ModelAdmin):
    list_display = ('EmployeeNo', 'LastName', 'FirstName', 'CoCd', 'Status')
    list_filter = ('CoCd', 'Status')
    search_fields = ('EmployeeNo', 'LastName', 'FirstName', 'OntrackID')
    fieldsets = (
        ('Basic Info', {
            'fields': ('EmployeeNo', 'LastName', 'FirstName')
        }),
        ('Company Info', {
            'fields': ('CoCd', 'Status')
        }),
        ('Other', {
            'fields': ('OntrackID',)
        }),
    )

@admin.register(EbauPriceList)
class EbauPriceListAdmin(admin.ModelAdmin):
    list_display = ('ConditionType', 'SalesOrganization', 'DistributionChannel', 'Material', 'Customer', 'ValidFrom', 'ValidTo')
    list_filter = ('ConditionType', 'SalesOrganization', 'DistributionChannel', 'SalesGroup')
    search_fields = ('Material', 'Customer')
    fieldsets = (
        ('Key Fields', {
            'fields': ('ConditionType', 'SalesOrganization', 'DistributionChannel', 'SalesGroup', 'Material', 'Customer')
        }),
        ('Validity', {
            'fields': ('ValidFrom', 'ValidTo')
        }),
        ('Pricing', {
            'fields': ('Rate', 'ConditionCurrency', 'PricingUnit', 'UnitOfMeasure')
        }),
        ('Other', {
            'fields': ('ScaleBasis', 'DeletionIndicator')
        }),
        ('System Fields', {
            'fields': ('Status', 'CreatedOn', 'CreatedSource', 'LastUpdate', 'UpdatedSource')
        }),
    )
