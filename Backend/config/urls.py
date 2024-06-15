from django.contrib import admin
from django.urls import path, include   # Add include import


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("config.api_router")),

]
