from django.contrib import admin

from accounts.models import *
from django.contrib.auth.models import Group

admin.site.unregister(Group)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone_number', 'address')

class VerificationOtpAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'code', 'expires_in']

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'phone_number', 'appartment', 'street', 'pin_code']

admin.site.register(User, UserAdmin)
admin.site.register(VerificationOtp, VerificationOtpAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
