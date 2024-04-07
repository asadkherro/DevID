from django.urls import path
from .views import DashboardPieChartView

urlpatterns = [
    path('piechart/', DashboardPieChartView.as_view(), name='working_api'),
]
