from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.db.models import Sum, Count
from .models import QuotationStatus, Quotation, QuotationDetails, QuotationItemDetails

@admin.register(QuotationStatus)
class QuotationStatusAdmin(admin.ModelAdmin):
    list_display = ('QStatusID', 'QStatusName')
    search_fields = ('QStatusName',)

class QuotationItemDetailsInline(admin.TabularInline):
    model = QuotationItemDetails
    extra = 1
    fields = ('MaterialNumber', 'MaterialDescription', 'OrderQuantity', 'PricePer', 'OrderValue', 'IsDeleted')
    readonly_fields = ('OrderValue',)

class QuotationDetailsInline(admin.StackedInline):
    model = QuotationDetails
    extra = 0
    fields = (
        ('QuoteRevisionNo', 'QuoteRevisionDate'), 
        ('SalesOrganization_id', 'SalesGroup'),
        ('SoldToCustomerNumber', 'ShipToCustomerNumber'),
        ('CustomerName', 'CustomerName2'),
        ('TermOfPayment', 'Incoterms', 'IncotermsPart2'),
        ('TradingCurrency', 'QuoteValidFrom', 'QuoteValidUntil'),
        ('DeliveryDate', 'CustomerPONumber'),
        'ApprovalStatus', 'Version'
    )

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('QuoteID', 'QuotationNo', 'CustomerNumber', 'Date', 'QStatusID', 'total_value', 'created_by', 'last_modified_by', 'is_valid', 'actions_column')
    list_filter = ('QStatusID', 'Date', 'created_by')
    search_fields = ('QuoteID', 'QuotationNo', 'CustomerNumber', 'CustomerEmail')
    readonly_fields = ('QuoteID', 'QuotationNo', 'CreationDate', 'total_value', 'is_valid')
    fieldsets = (
        (None, {
            'fields': (('QuoteID', 'QuotationNo'), ('CustomerNumber', 'CustomerEmail'), 
                       ('LastRevision', 'Version'), ('Date', 'CreationDate'),
                       'CustomerInquiryNo')
        }),
        ('Status and Values', {
            'fields': ('QStatusID', 'total_value', 'GSTVATValue', 'TotalDiscount')
        }),
        ('Validity', {
            'fields': (('QuoteValidFrom', 'QuoteValidUntil'), 'is_valid')
        }),
        ('Additional Information', {
            'fields': ('Remarks', 'rejection_reason')
        }),
        ('User Information', {
            'fields': ('created_by', 'last_modified_by')
        }),
    )
    inlines = [QuotationDetailsInline]

    def is_valid(self, obj):
        return obj.is_valid
    is_valid.boolean = True
    is_valid.short_description = 'Is Valid'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.last_modified_by = request.user
        super().save_model(request, obj, form, change)

    def actions_column(self, obj):
        return format_html(
            '<a class="button" href="{}">Approve</a>&nbsp;'
            '<a class="button" href="{}">Reject</a>&nbsp;'
            '<a class="button" href="{}">Submit</a>&nbsp;'
            '<a class="button" href="{}">Cancel</a>&nbsp;'
            '<a class="button" href="{}">Revise</a>',
            reverse('admin:approve_quotation', args=[obj.pk]),
            reverse('admin:reject_quotation', args=[obj.pk]),
            reverse('admin:submit_quotation', args=[obj.pk]),
            reverse('admin:cancel_quotation', args=[obj.pk]),
            reverse('admin:revise_quotation', args=[obj.pk]),
        )
    actions_column.short_description = 'Actions'
    actions_column.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/approve/', self.admin_site.admin_view(self.approve_view), name='approve_quotation'),
            path('<path:object_id>/reject/', self.admin_site.admin_view(self.reject_view), name='reject_quotation'),
            path('<path:object_id>/submit/', self.admin_site.admin_view(self.submit_view), name='submit_quotation'),
            path('<path:object_id>/cancel/', self.admin_site.admin_view(self.cancel_view), name='cancel_quotation'),
            path('<path:object_id>/revise/', self.admin_site.admin_view(self.revise_view), name='revise_quotation'),
        ]
        return custom_urls + urls

    def approve_view(self, request, object_id):
        quotation = self.get_object(request, object_id)
        quotation.approve(request.user)
        self.message_user(request, "Quotation approved successfully.")
        return redirect('admin:quotation_quotation_changelist')

    def reject_view(self, request, object_id):
        quotation = self.get_object(request, object_id)
        if request.method == 'POST':
            reason = request.POST.get('rejection_reason', '')
            if reason:
                quotation.reject(request.user, reason)
                self.message_user(request, "Quotation rejected successfully.")
                return redirect('admin:quotation_quotation_changelist')
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['quotation'] = quotation
        return TemplateResponse(request, 'admin/quotation/quotation/reject.html', context)

    def submit_view(self, request, object_id):
        quotation = self.get_object(request, object_id)
        quotation.submit(request.user)
        self.message_user(request, "Quotation submitted successfully.")
        return redirect('admin:quotation_quotation_changelist')

    def cancel_view(self, request, object_id):
        quotation = self.get_object(request, object_id)
        quotation.cancel(request.user)
        self.message_user(request, "Quotation cancelled successfully.")
        return redirect('admin:quotation_quotation_changelist')

    def revise_view(self, request, object_id):
        quotation = self.get_object(request, object_id)
        quotation.revise(request.user)
        self.message_user(request, "Quotation revised successfully.")
        return redirect('admin:quotation_quotation_changelist')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            item_count=Count('details__items'),
            total_order_value=Sum('details__items__OrderValue')
        )
        return queryset

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        metrics = {
            'total_quotations': Count('id'),
            'total_value': Sum('total_value'),
            'average_value': Sum('total_value') / Count('id'),
        }
        response.context_data['summary'] = dict(
            qs.aggregate(**metrics)
        )
        return response

@admin.register(QuotationDetails)
class QuotationDetailsAdmin(admin.ModelAdmin):
    list_display = ('QuotationDetailsId', 'get_quote_id', 'QuoteRevisionNo', 'get_sales_organization', 'SoldToCustomerNumber', 'TermOfPayment', 'DeliveryDate')
    list_filter = ('SalesOrganization_id', 'QuoteRevisionDate', 'TermOfPayment', 'DeliveryDate')
    search_fields = ('QuoteID__QuotationNo', 'SoldToCustomerNumber', 'CustomerName', 'TermOfPayment')
    inlines = [QuotationItemDetailsInline]

    def get_quote_id(self, obj):
        return obj.QuoteID.QuoteID
    get_quote_id.short_description = 'Quote ID'
    get_quote_id.admin_order_field = 'QuoteID__QuoteID'

    def get_sales_organization(self, obj):
        return obj.SalesOrganization_id.SalesOrganizationName
    get_sales_organization.short_description = 'Sales Organization'
    get_sales_organization.admin_order_field = 'SalesOrganization_id__SalesOrganizationName'

@admin.register(QuotationItemDetails)
class QuotationItemDetailsAdmin(admin.ModelAdmin):
    list_display = ('QuoteItemId', 'get_quotation_no', 'MaterialNumber', 'OrderQuantity', 'PricePer', 'OrderValue', 'IsDeleted')
    list_filter = ('IsDeleted', 'UnitOfMeasure')
    search_fields = ('MaterialNumber', 'MaterialDescription', 'QuotationDetailsId__QuoteID__QuotationNo')
    readonly_fields = ('OrderValue',)

    def get_quotation_no(self, obj):
        return obj.QuotationDetailsId.QuoteID.QuotationNo
    get_quotation_no.short_description = 'Quotation No'
    get_quotation_no.admin_order_field = 'QuotationDetailsId__QuoteID__QuotationNo'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            total_order_value=Sum('OrderValue')
        )
        return queryset

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        metrics = {
            'total_order_value': Sum('OrderValue'),
            'total_quantity': Sum('OrderQuantity'),
            'average_price': Sum('OrderValue') / Sum('OrderQuantity'),
        }
        response.context_data['summary'] = dict(
            qs.aggregate(**metrics)
        )
        return response
