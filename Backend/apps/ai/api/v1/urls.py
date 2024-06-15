from django.urls import path

from apps.ai.api.v1.views import PredictDeviceCategoryView

urlpatterns = [
  path('predict-category/' , PredictDeviceCategoryView.as_view() , name='predict_category')
]
