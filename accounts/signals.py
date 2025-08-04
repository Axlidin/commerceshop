from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import *
from accounts.utils import generate_otp_code
from core.settings.base import VERIFICATION_OTP_EXPIRATION_TIME
from accounts.tasks import send_otp_code_to_email

@receiver(post_save, sender=User)
def create_verifation_otp(sender, instance, created, **kwargs):
    if created:
        code = generate_otp_code()
        VerificationOtp.objects.create(user=instance, type=VerificationOtp.VerificationType.REGISTER,
                                       code=code, expires_in=datetime.now() + timedelta(minutes=VERIFICATION_OTP_EXPIRATION_TIME))
        send_otp_code_to_email(code=code, email=instance.email)
