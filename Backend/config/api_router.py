from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter() if settings.DEBUG else SimpleRouter()


app_name = "api"

urlpatterns = [
    path("v1/", include("apps.scan.api.v1.urls")),
    path("v1/", include("apps.ai.api.v1.urls")),
    path("v1/", include("apps.dashboard.api.v1.urls")),
] + router.urls
