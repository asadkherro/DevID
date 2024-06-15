from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.api.v1.views import LoginView , VerifyOTP


urlpatterns = [
  path("login/" , LoginView.as_view() , name="login"),
  path("verify-otp/" , VerifyOTP.as_view() , name="verify_otp"),
 
]
