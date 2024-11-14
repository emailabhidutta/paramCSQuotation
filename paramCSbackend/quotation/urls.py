from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import home, dashboard_view  # Import the dashboard view

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/core/', include('core.urls')),
    path('api/quotation/', include('quotation.urls')),
    path('api/company/', include('company.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/', dashboard_view, name='dashboard'),  # Add this line
]
