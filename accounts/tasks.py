from celery import shared_task
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from core.settings.base import EMAIL_HOST

@shared_task
def send_otp_code_to_email(code, email):
    message = f"Your verification code is {code}"
    send_mail(
        subject=_("Register Verification OTP code"),
        message=message,
        from_email=EMAIL_HOST,
        recipient_list=[email],
    )
