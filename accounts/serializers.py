from django.utils import timezone
from rest_framework import serializers
from accounts.models import *
from accounts.utils import generate_otp_code, send_email
from core.settings.base import VERIFICATION_OTP_EXPIRATION_TIME

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

    # def create(self, validated_data):
    #     user = User.objects.filter(email=validated_data.get("email"), is_active=False)
    #     if user.exists():
    #         sms = VerificationOtp.objects.get(
    #             user=user, type=VerificationOtp.VerificationType.REGISTER,
    #             expires_in__lt=timezone.now(), is_active=True
    #         )
    #         if sms:
    #             sms.expires_in = timezone.now() + VERIFICATION_OTP_EXPIRATION_TIME
    #             code = generate_otp_code()
    #             sms.code = code
    #             send_email(code=code, email=user.email)
    #
    #     return self.create(self, validated_data)

    # def create(self, validated_data):
    #     email = validated_data.get("email")
    #     user = User.objects.filter(email=email, is_active=False)
    #
    #     if user.exists():
    #         existing_user = user.first()
    #         sms = VerificationOtp.objects.filter(
    #             user=existing_user,
    #             type=VerificationOtp.VerificationType.REGISTER,
    #             expires_in__lt=timezone.now(),
    #             is_active=True
    #         ).last()
    #         if sms:
    #             sms.expires_in = timezone.now() + VERIFICATION_OTP_EXPIRATION_TIME
    #             code = generate_otp_code()
    #             sms.code = code
    #             sms.save()
    #             send_email(code=code, email=email)
    #         return existing_user  # Mavjud foydalanuvchini qaytarish
    #
    #     # Yangi foydalanuvchi yaratish
    #     validated_data["is_active"] = False
    #     user = User.objects.create_user(**validated_data)
    #
    #     code = generate_otp_code()
    #     VerificationOtp.objects.create(
    #         user=user,
    #         type=VerificationOtp.VerificationType.REGISTER,
    #         code=code,
    #         expires_in=timezone.now() + VERIFICATION_OTP_EXPIRATION_TIME,
    #         is_active=True
    #     )
    #     send_email(code=code, email=user.email)
    #     return user
    #

class VerifyOtpSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    email = serializers.CharField(required=True)
    verify_type = serializers.ChoiceField(choices=VerificationOtp.VerificationType)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    verification = serializers.IntegerField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError("Passwords do not match")
        return attrs