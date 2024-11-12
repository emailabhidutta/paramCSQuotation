from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrencyViewSet, CurrencyExchangeViewSet

router = DefaultRouter()
router.register(r'currencies', CurrencyViewSet)
router.register(r'exchanges', CurrencyExchangeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]