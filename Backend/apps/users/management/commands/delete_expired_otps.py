from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import OTP

class Command(BaseCommand):
    help = 'Deletes expired OTP instances that are older than 2 hours'

    def handle(self, *args, **kwargs):
        expired_otps = OTP.objects.filter(created_at__lt=timezone.now() - timezone.timedelta(hours=2))
        count, _ = expired_otps.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} expired OTPs'))
