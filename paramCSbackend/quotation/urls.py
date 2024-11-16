from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    dashboard_view,
    QuotationStatusViewSet,
    QuotationViewSet,
    QuotationDetailsViewSet,
    QuotationItemDetailsViewSet
)

router = DefaultRouter()
router.register(r'status', QuotationStatusViewSet)
router.register(r'quotations', QuotationViewSet)
router.register(r'details', QuotationDetailsViewSet)
router.register(r'items', QuotationItemDetailsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', dashboard_view, name='dashboard'),
    # The following actions are automatically included by the router:
    # path('quotations/<pk>/approve/', QuotationViewSet.as_view({'post': 'approve'}), name='quotation-approve'),
    # path('quotations/<pk>/reject/', QuotationViewSet.as_view({'post': 'reject'}), name='quotation-reject'),
    # path('quotations/<pk>/revise/', QuotationViewSet.as_view({'post': 'revise'}), name='quotation-revise'),
    # path('items/<pk>/soft-delete/', QuotationItemDetailsViewSet.as_view({'post': 'soft_delete'}), name='item-soft-delete'),
]
