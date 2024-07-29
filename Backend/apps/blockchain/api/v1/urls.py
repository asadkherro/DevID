from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeployContractView, DeviceViewSet

# SetValueView, GetValueView , DeleteDeviceView

router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="device")

urlpatterns = [
    path("deploy/", DeployContractView.as_view(), name="deploy_contract"),
    # path('contract/addDevices/', SetValueView.as_view(), name='set_value'),
    # path('contract/getDevices/', GetValueView.as_view(), name='get_value'),
    # path('contract/delete/<str:id>/', DeleteDeviceView.as_view(), name='delete_device'),
    # path('contract/update/<str:id>/', DeleteDeviceView.as_view(), name='delete_device'),
    path("", include(router.urls)),
]
