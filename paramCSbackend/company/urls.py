from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, CompanyViewSet, SalesOrganizationViewSet, AccountGroupViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'sales-organizations', SalesOrganizationViewSet)
router.register(r'account-groups', AccountGroupViewSet)

urlpatterns = [
    path('api/v1/company/', include([
        path('', include(router.urls)),
        path('countries/active/', CountryViewSet.as_view({'get': 'active_countries'}), name='active-countries'),
        path('companies/<str:pk>/toggle-active/', CompanyViewSet.as_view({'post': 'toggle_active'}), name='toggle-company-active'),
        path('sales-organizations/by-company/', SalesOrganizationViewSet.as_view({'get': 'by_company'}), name='sales-orgs-by-company'),
        path('account-groups/by-sales-org/', AccountGroupViewSet.as_view({'get': 'by_sales_org'}), name='account-groups-by-sales-org'),
    ])),
]
