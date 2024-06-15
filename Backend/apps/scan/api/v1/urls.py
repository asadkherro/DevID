from django.urls import path
from .views import SubnetScanView , PythonScanView , OsScanView

urlpatterns = [
    path('test/', SubnetScanView.as_view(), name='working_api'),
    path('normal/' , PythonScanView.as_view() , name='normal'),
    path('advance/' , OsScanView.as_view() , name='advance')
]
