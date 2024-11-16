from django.contrib import admin
from .models import QuotationStatus, Quotation, QuotationDetails, QuotationItemDetails

@admin.register(QuotationStatus)
class QuotationStatusAdmin(admin.ModelAdmin):
    list_display = ('QStatusID', 'QStatusName')
    search_fields = ('QStatusID', 'QStatusName')

class QuotationItemDetailsInline(admin.TabularInline):
    model = QuotationItemDetails
    extra = 1
    fields = ('MaterialNumber', 'MaterialDescription', 'OrderQuantity', 'PricePer', 'UnitOfMeasure', 'OrderValue', 'IsDeleted')
    readonly_fields = ('OrderValue',)

class QuotationDetailsInline(admin.StackedInline):
    model = QuotationDetails
    extra = 1
    fields = ('QuoteRevisionNo', 'SalesOrganization', 'Customer', 'ShipToCustomerNumber', 'TradingCurrency', 'DeliveryDate')

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('QuoteId', 'QuotationNo', 'CustomerNumber', 'Date', 'QStatusID', 'total_value', 'Version')
    list_filter = ('QStatusID', 'Date', 'CreationDate')
    search_fields = ('QuoteId', 'QuotationNo', 'CustomerNumber')
    inlines = [QuotationDetailsInline]
    readonly_fields = ('CreationDate', 'created_by', 'last_modified_by', 'total_value')
    fieldsets = (
        ('Basic Info', {
            'fields': ('QuoteId', 'QuotationNo', 'CustomerNumber', 'LastRevision', 'CustomerInquiryNo', 'Date')
        }),
        ('Dates', {
            'fields': ('CreationDate', 'QuoteValidFrom', 'QuoteValidUntil')
        }),
        ('Status and Values', {
            'fields': ('QStatusID', 'total_value', 'GSTVATValue', 'TotalDiscount')
        }),
        ('Other Details', {
            'fields': ('CustomerEmail', 'Version', 'Remarks', 'rejection_reason')
        }),
        ('System Fields', {
            'fields': ('created_by', 'last_modified_by'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.last_modified_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, QuotationDetails):
                if not change:
                    instance.created_by = request.user
                instance.last_modified_by = request.user
            instance.save()
        formset.save_m2m()

@admin.register(QuotationDetails)
class QuotationDetailsAdmin(admin.ModelAdmin):
    list_display = ('QuotationDetailsId', 'QuoteId', 'QuoteRevisionNo', 'SalesOrganization', 'Customer')
    list_filter = ('SalesOrganization', 'ApprovalStatus')
    search_fields = ('QuotationDetailsId', 'QuoteId__QuotationNo', 'Customer')
    inlines = [QuotationItemDetailsInline]

@admin.register(QuotationItemDetails)
class QuotationItemDetailsAdmin(admin.ModelAdmin):
    list_display = ('QuoteItemId', 'QuotationDetailsId', 'MaterialNumber', 'OrderQuantity', 'OrderValue', 'IsDeleted')
    list_filter = ('UnitOfMeasure', 'IsDeleted')
    search_fields = ('QuoteItemId', 'MaterialNumber', 'MaterialDescription')
    readonly_fields = ('OrderValue',)

    def save_model(self, request, obj, form, change):
        obj.OrderValue = obj.OrderQuantity * obj.PricePer
        super().save_model(request, obj, form, change)
