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
]
