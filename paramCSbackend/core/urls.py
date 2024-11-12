from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, RightsViewSet, UserRightsViewSet, CustomUserViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'rights', RightsViewSet)
router.register(r'user-rights', UserRightsViewSet)
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
