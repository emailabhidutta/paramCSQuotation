from django.contrib import admin
from django.utils.html import format_html
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
    fields = ('QuoteRevisionNo', 'SalesOrganization', 'SoldToCustomerNumber', 'ShipToCustomerNumber', 'TradingCurrency', 'DeliveryDate')

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('QuoteId', 'QuotationNo', 'CustomerNumber', 'Date', 'status_with_color', 'total_value', 'Version', 'is_valid')
    list_filter = ('QStatusID', 'Date', 'CreationDate')
    search_fields = ('QuoteId', 'QuotationNo', 'CustomerNumber')
    inlines = [QuotationDetailsInline]
    readonly_fields = ('CreationDate', 'created_by', 'last_modified_by', 'total_value', 'is_valid')
    fieldsets = (
        ('Basic Info', {
            'fields': ('QuoteId', 'QuotationNo', 'CustomerNumber', 'LastRevision', 'CustomerInquiryNo', 'Date')
        }),
        ('Dates', {
            'fields': ('CreationDate', 'QuoteValidFrom', 'QuoteValidUntil')
        }),
        ('Status and Values', {
            'fields': ('QStatusID', 'total_value', 'GSTVATValue', 'TotalDiscount', 'is_valid')
        }),
        ('Other Details', {
            'fields': ('CustomerEmail', 'Version', 'Remarks', 'rejection_reason')
        }),
        ('System Fields', {
            'fields': ('created_by', 'last_modified_by'),
            'classes': ('collapse',)
        }),
    )

    def status_with_color(self, obj):
        colors = {
            'Draft': 'blue',
            'Submitted': 'orange',
            'Approved': 'green',
            'Rejected': 'red',
            'Cancelled': 'gray'
        }
        color = colors.get(obj.QStatusID.QStatusName, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.QStatusID.QStatusName)
    status_with_color.short_description = 'Status'

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
    list_display = ('QuotationDetailsId', 'QuoteId', 'QuoteRevisionNo', 'SalesOrganization', 'SoldToCustomerNumber')
    list_filter = ('SalesOrganization', 'ApprovalStatus')
    search_fields = ('QuotationDetailsId', 'QuoteId__QuotationNo', 'SoldToCustomerNumber')
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

    actions = ['mark_as_deleted', 'mark_as_not_deleted']

    def mark_as_deleted(self, request, queryset):
        queryset.update(IsDeleted=True)
    mark_as_deleted.short_description = "Mark selected items as deleted"

    def mark_as_not_deleted(self, request, queryset):
        queryset.update(IsDeleted=False)
    mark_as_not_deleted.short_description = "Mark selected items as not deleted"
