from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login

from apps.users.models import User, OTP
from apps.core.renderer import CustomJSONRenderer

from .serializers import LoginSerializer, VerifyOTPSerializer
from apps.users.utils import send_otp


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    # renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response("OTP sent to your Email", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifyOTPSerializer
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data["otp"]
            user = User.objects.get(email=serializer.validated_data["email"])
            print(user)
            print(otp_code)
            try:
                otp = OTP.objects.get(code=otp_code, user=user)
                print(otp)
                if otp.is_expired:
                    return Response(
                        {"detail": "OTP has expired"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user = otp.user
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                otp.delete()
                return Response(
                    {
                        "detail": "OTP Verified",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                    status=status.HTTP_200_OK,
                )

            except OTP.DoesNotExist:
                return Response(
                    {"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
