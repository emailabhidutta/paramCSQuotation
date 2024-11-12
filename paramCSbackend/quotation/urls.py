from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuotationStatusViewSet, QuotationViewSet, QuotationDetailsViewSet, QuotationItemDetailsViewSet

router = DefaultRouter()
router.register(r'statuses', QuotationStatusViewSet)
router.register(r'quotations', QuotationViewSet)
router.register(r'details', QuotationDetailsViewSet)
router.register(r'items', QuotationItemDetailsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]