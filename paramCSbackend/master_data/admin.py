from django.contrib import admin
from .models import CustomerMaster, MaterialMaster

@admin.register(CustomerMaster)
class CustomerMasterAdmin(admin.ModelAdmin):
    list_display = ('CustomerNumber', 'CustomerName1', 'SalesOrg', 'City', 'Country')
    list_filter = ('SalesOrg', 'Country', 'CustomerClass', 'KeyAccount')
    search_fields = ('CustomerNumber', 'CustomerName1', 'CustomerName2', 'SearchTerm')
    fieldsets = (
        ('Basic Info', {
            'fields': ('CustomerNumber', 'CustomerName1', 'CustomerName2', 'SearchTerm')
        }),
        ('Organization', {
            'fields': ('SalesOrg', 'AccountGroup', 'CustomerClass', 'KeyAccount', 'SalesGroup')
        }),
        ('Address', {
            'fields': ('HouseStreetName', 'City', 'Country')
        }),
        ('Business Terms', {
            'fields': ('CustPriceProc', 'TermOfPayment', 'Incoterms', 'IncotermsPort', 'TradingCurrency')
        }),
        ('Status', {
            'fields': ('CustomerBlocked', 'CustomerDeleted')
        }),
    )

@admin.register(MaterialMaster)
class MaterialMasterAdmin(admin.ModelAdmin):
    list_display = ('MaterialNumber', 'MaterialDescription', 'Plant', 'ProductGroup', 'UnitOfMeasure')
    list_filter = ('Plant', 'ProductGroup', 'ProductType', 'LifeCycleFlag')
    search_fields = ('MaterialNumber', 'MaterialDescription', 'DrawingNumber')
    fieldsets = (
        ('Basic Info', {
            'fields': ('MaterialNumber', 'MaterialDescription', 'Plant', 'CrossPlantStatus')
        }),
        ('Details', {
            'fields': ('DrawingNumber', 'FourDigitDescription', 'BasicMaterial', 'BasicMatDescription')
        }),
        ('Classification', {
            'fields': ('MachineType', 'ProductGroup', 'ProductType', 'LifeCycleFlag', 'ProductHierarchy')
        }),
        ('Other', {
            'fields': ('PlantOldMaterialNumber', 'UnitOfMeasure')
        }),
    )
