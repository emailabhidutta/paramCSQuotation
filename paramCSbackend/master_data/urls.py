from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerMasterViewSet, MaterialMasterViewSet

router = DefaultRouter()
router.register(r'customers', CustomerMasterViewSet)
router.register(r'materials', MaterialMasterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
