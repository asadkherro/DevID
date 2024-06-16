from django.urls import path
from .views import DashboardPieChartView

urlpatterns = [
    path('dashboard/piechart/', DashboardPieChartView.as_view(), name='working_api'),
]
