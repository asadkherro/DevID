from django.urls import path
from .views import SubnetScanView , PythonScanView , OsScanView , CurrentDeviceView

urlpatterns = [
    path('scan/test/', SubnetScanView.as_view(), name='working_api'),
    path('scan/normal/' , PythonScanView.as_view() , name='normal'),
    path('scan/advance/' , OsScanView.as_view() , name='advance'),
    path('scan/current/' , CurrentDeviceView.as_view() , name='advance')
]
