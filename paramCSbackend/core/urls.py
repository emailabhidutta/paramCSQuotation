from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RoleViewSet, RightsViewSet, UserRightsViewSet, CustomUserViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'rights', RightsViewSet)
router.register(r'user-rights', UserRightsViewSet)
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
