from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, CompanyViewSet, SalesOrganizationViewSet, AccountGroupViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'sales-organizations', SalesOrganizationViewSet)
router.register(r'account-groups', AccountGroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
