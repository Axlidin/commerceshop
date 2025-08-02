from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import *
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
admin.site.unregister(Group)

class UserAdmin_(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "email")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "address", "phone_number")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2"),
            },
        ),
    )
class VerificationOtpAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'code', 'expires_in']

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'phone_number', 'appartment', 'street', 'pin_code']

admin.site.register(User, UserAdmin_)
admin.site.register(VerificationOtp, VerificationOtpAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
