from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from accounts.managers import UserManager
from accounts.utils import CheckVerifacationOtp
class User(AbstractUser):
    email = models.EmailField(_("Email address"), unique=True)
    phone_number = models.CharField(max_length=20, verbose_name=_("Phone number"), validators=[RegexValidator(r'^\+?1?\d{9,12}$')])
    address = models.TextField(max_length=100, verbose_name=_("Address"))
    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=True, blank=True
    )
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class VerificationOtp(models.Model):
    class VerificationType(models.TextChoices):
        REGISTER = 'register', _('Register')
        RESET_PASSWORD = 'reset_password', _('Reset password')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='verification_otp')
    # code = models.CharField(_("Otp code"), validators=[RegexValidator(r'^\d{6}$')])
    code = models.IntegerField(_("Otp code"), validators=[CheckVerifacationOtp])
    type = models.CharField(_("Verification type"), max_length=60, choices=VerificationType.choices)
    expires_in = models.DateTimeField(_("Expires in"))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} | {self.code}"

    class Meta:
        verbose_name = _("Verification Otp")
        verbose_name_plural = _("Verification Otps")

class UserAddress(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_address')
    name = models.CharField(_("Name"), max_length=120)
    phone_number = models.CharField(_("Phone number"), max_length=20, validators=[RegexValidator(r'^\+?1?\d{9,12}$')])
    appartment = models.CharField(_("Appartment"), max_length=120)
    street = models.TextField(_("Street"))
    pin_code = models.CharField(_("Pin code"), max_length=60)
    # city

    def __str__(self):
        return f"{self.user.id} | {self.name}"

    class Meta:
        verbose_name = _("User Address")
        verbose_name_plural = _("User Addresses")