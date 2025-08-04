import secrets
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from core.settings.base import EMAIL_HOST

def CheckVerifacationOtp(value):
   if len(str(value)) != 6:
       raise ValidationError(_("Otp code must be 6 digits"))



def generate_otp_code():
    numbers = "123456789"
    return "".join(secrets.choice(numbers) for _ in range(6))