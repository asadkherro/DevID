from django.urls import path
from .views import DeployContractView, SetValueView, GetValueView

urlpatterns = [
    path('deploy/', DeployContractView.as_view(), name='deploy_contract'),
    path('set_value/', SetValueView.as_view(), name='set_value'),
    path('get_value/', GetValueView.as_view(), name='get_value'),
]
