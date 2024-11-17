from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import (
    dashboard_view,
    QuotationStatusViewSet,
    QuotationViewSet,
    QuotationDetailsViewSet,
    QuotationItemDetailsViewSet
)

# Main router
router = DefaultRouter()
router.register(r'status', QuotationStatusViewSet)
router.register(r'quotations', QuotationViewSet, basename='quotation')

# Nested router for quotation details
quotation_router = routers.NestedSimpleRouter(router, r'quotations', lookup='quotation')
quotation_router.register(r'details', QuotationDetailsViewSet, basename='quotation-details')

# Nested router for quotation item details
details_router = routers.NestedSimpleRouter(quotation_router, r'details', lookup='detail')
details_router.register(r'items', QuotationItemDetailsViewSet, basename='quotation-items')

app_name = 'quotation'  # Add namespace

urlpatterns = [
    path('api/v1/', include([
        path('', include(router.urls)),
        path('', include(quotation_router.urls)),
        path('', include(details_router.urls)),
        path('dashboard/', dashboard_view, name='dashboard'),
        
        # Custom action endpoints
        path('quotations/<str:pk>/submit/', QuotationViewSet.as_view({'post': 'submit'}), name='quotation-submit'),
        path('quotations/<str:pk>/approve/', QuotationViewSet.as_view({'post': 'approve'}), name='quotation-approve'),
        path('quotations/<str:pk>/reject/', QuotationViewSet.as_view({'post': 'reject'}), name='quotation-reject'),
        path('quotations/<str:pk>/cancel/', QuotationViewSet.as_view({'post': 'cancel'}), name='quotation-cancel'),
        path('quotations/<str:pk>/revise/', QuotationViewSet.as_view({'post': 'revise'}), name='quotation-revise'),
        
        # Additional custom endpoints
        path('quotations/customer-details/', QuotationViewSet.as_view({'get': 'get_customer_details'}), name='customer-details'),
        path('quotations/item-rates/', QuotationViewSet.as_view({'get': 'get_item_rates'}), name='item-rates'),
        path('quotations/material-details/', QuotationViewSet.as_view({'get': 'get_material_details'}), name='material-details'),
    ])),
]
