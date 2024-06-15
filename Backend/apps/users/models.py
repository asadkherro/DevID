import uuid
import string
import random
import time

from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel
from django.utils import timezone


class OTP(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6 , unique=True)

    def __str__(self):
        return f"{self.user.email}-{self.code}"

    @property
    def is_expired(self):
        expiration_time = self.created_at + timezone.timedelta(minutes=3)
        return timezone.now() > expiration_time

    @staticmethod
    def generate_code():
        characters = string.digits + string.ascii_lowercase
        start_time = time.time()
        while True:
            code = "".join(random.choices(characters, k=6))
            if not OTP.objects.filter(code=code).exists():
                break
            current_time = time.time()
            if current_time - start_time >= 15:
                raise TimeoutError("Timeout occurred while generating OTP code")
        return code
    @classmethod
    def create_otp(cls, user):
        code = cls.generate_code()
        return cls.objects.create(user=user, code=code)
