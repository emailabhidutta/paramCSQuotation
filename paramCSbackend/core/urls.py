from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, RightsViewSet, UserRightsViewSet, CustomUserViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'rights', RightsViewSet)
router.register(r'user-rights', UserRightsViewSet)
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/me/', CustomUserViewSet.as_view({'get': 'me'}), name='user-me'),
    path('users/<int:pk>/change-password/', CustomUserViewSet.as_view({'post': 'change_password'}), name='user-change-password'),
    path('users/reset-password/', CustomUserViewSet.as_view({'post': 'reset_password'}), name='user-reset-password'),
    path('users/set-new-password/', CustomUserViewSet.as_view({'post': 'set_new_password'}), name='user-set-new-password'),
]
