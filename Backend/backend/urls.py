from django.contrib import admin
from django.urls import path, include   # Add include import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/scan/', include('scan.urls')),
    path('api/v1/dashboard/' , include('dashboard.urls'))
]
