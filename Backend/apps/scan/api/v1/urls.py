from django.urls import path
from .views import SubnetScanView , PythonScanView , OsScanView

urlpatterns = [
    path('scan/test/', SubnetScanView.as_view(), name='working_api'),
    path('scan/normal/' , PythonScanView.as_view() , name='normal'),
    path('scna/advance/' , OsScanView.as_view() , name='advance')
]
