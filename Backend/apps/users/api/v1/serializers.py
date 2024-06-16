from rest_framework import serializers

from apps.users.models import User , OTP
from apps.users.utils import send_otp

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self , value):
        if User.objects.filter(email=value).exists():
            user = User.objects.get(email=value)
            send_otp(user=user)
            return value
        raise serializers.ValidationError("Invalid Email Address")



class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)