from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView ,TokenBlacklistView

from apps.users.api.v1.views import LoginView , VerifyOTP


urlpatterns = [
  path("login/" , LoginView.as_view() , name="login"),
  path("verify-otp/" , VerifyOTP.as_view() , name="verify_otp"),
 path("token/refresh/" , TokenRefreshView.as_view() , name="refresh_token"),
  path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

]
