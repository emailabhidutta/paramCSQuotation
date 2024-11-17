from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('dashboard/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=True), name='index'),
    path('api/core/', include('core.urls')),
    path('', include('quotation.urls', namespace='quotation')),
    path('api/company/', include('company.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/master-data/', include('master_data.urls')),  # Add this line
    
    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
