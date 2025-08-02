from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from accounts.models import *
from accounts.serializers import *

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class VerifyOtpView(APIView):
    serializer_class = VerifyOtpSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = VerifyOtpSerializer(data=data)
            if not serializer.is_valid():
                raise APIException(detail="Data is not valid")
            user = User.objects.get(email=data.get("email"))
            verify_type = data.get("verify_type")
            sms = VerificationOtp.objects.filter(
                Q(user=user) &
                Q(type=verify_type) &
                Q(code=data.get("code"))
            )
            if not sms.exists():
                return Response(data={"message": "otp_code_not_found"}, status=status.HTTP_400_BAD_REQUEST)

            if not sms.filter(is_active=True).exists():
                return Response(data={"message": "otp_code_already_activated"}, status=status.HTTP_400_BAD_REQUEST)

            if not sms.filter(expires_in__gte=timezone.now()):
                return Response(data={"message": "otp_code_expired"}, status=status.HTTP_400_BAD_REQUEST)

            sms_obj = sms.last()
            user.is_active = True
            user.save()
            sms_obj.is_active = False
            sms_obj.save()
            return Response(data={"message": "otp_code_activated", "verification": sms_obj.id})

        except User.DoesNotExist:
            raise APIException(detail="User does not exist")

        except Exception as e:
            raise e


class ResetPasswordStartView(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = ResetPasswordSerializer(data=data)
            if not serializer.is_valid():
                return Response(data={"message": "Email is not valid"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(email=data.get("email"))
            code = generate_otp_code()
            VerificationOtp.objects.create(user=user, type=VerificationOtp.VerificationType.RESET_PASSWORD,
                                           code=code, expires_in=timezone.now() + timezone.timedelta(
                    minutes=VERIFICATION_OTP_EXPIRATION_TIME))
            send_email(code=code, email=user.email)
            return Response(data={"message": "sent_otp_code_to_email"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            raise APIException(detail="User does not exist")

        except Exception as e:
            raise e

class ResetPasswordFinishView(APIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = ResetPasswordConfirmSerializer(data=data)
            if not serializer.is_valid():
                return Response(data={"message": "Data is not valid", "result": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(email=data.get("email"))
            sms_code = VerificationOtp.objects.get(user=user, type=VerificationOtp.VerificationType.RESET_PASSWORD, id=data.get("verification"))
            if sms_code.is_active is True:
                return Response(data={"message": "otp_code_is_activated_yet"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(data.get("password"))
            user.save()
            return Response(data={"message": "password_changed_successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise APIException(detail="User does not exist")
        except VerificationOtp.DoesNotExist:
            raise APIException(detail="Verification code does not exist")