from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import *
from accounts.utils import generate_otp_code, send_email
from core.settings.base import VERIFICATION_OTP_EXPIRATION_TIME


@receiver(post_save, sender=User)
def create_verifation_otp(sender, instance, created, **kwargs):
    if created:
        code = generate_otp_code()
        VerificationOtp.objects.create(user=instance, type=VerificationOtp.VerificationType.REGISTER,
                                       code=code, expires_in=datetime.now() + timedelta(minutes=VERIFICATION_OTP_EXPIRATION_TIME))
        send_email(code=code, email=instance.email)
        print("Verification Otp created")