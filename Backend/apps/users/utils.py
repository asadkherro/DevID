
from django.core.mail import send_mail
from django.conf import settings

from apps.users.models import OTP, User

def send_otp(user:User):
    otp_obj = OTP.create_otp(user=user)
    username = user.username if user.username is not None else user.email.split('@')[0]  
    otp_code = otp_obj.code
    html_message = f"""
    <html>
    <head></head>
    <body>
        <p>Dear {username},</p>
        <p>To complete your login, please use the following One-Time Password (OTP):</p>
        <h2 style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;color:teal">{otp_code}</h2>
        <p>This OTP is valid for the next 3 minutes. Please do not share this code with anyone.</p>
        <br>
        <p>Best regards,<br>
        The DevID Team</p>
    </body>
    </html>
    """

    send_mail(
        subject="Your DevID One-Time Password (OTP)",
        message=f"Dear {username},\n\n"
                f"To complete your login, please use the following One-Time Password (OTP): {otp_code}\n\n"
                f"This OTP is valid for the next 3 minutes. Please do not share this code with anyone.\n\n"
                f"Best regards,\n"
                f"The DevID Team",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        html_message=html_message,
    )
