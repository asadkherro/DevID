from django.contrib import admin

from apps.users.models import OTP

class OTPAdmin(admin.ModelAdmin):
    list_display = [
        'get_user_email',
        'code',
        'is_expired',
        'created_at'
    ]

    @admin.display(description="User Email")
    def get_user_email(self , obj:OTP):
        return obj.user.email


admin.site.register(OTP , OTPAdmin)