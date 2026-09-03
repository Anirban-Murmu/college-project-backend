import secrets

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

from accounts.models import EmailOTP


OTP_EXPIRY_MINUTES = 5
MAX_OTP_ATTEMPTS = 5


class OTPService:

    # generate a 6-digit OTP
    @staticmethod
    def generate_otp():

        return f"{secrets.randbelow(1_000_000):06d}"


    # create a new OTP for the given email and if previous OTPs exist for the same email and purpose, invalidate them
    @staticmethod
    def create_otp(email, purpose):

        email = email.lower().strip()

        # Invalidate previous OTPs
        EmailOTP.objects.filter(
            email=email,
            purpose=purpose,
            is_verified=False
        ).update(
            is_verified=True
        )

        otp = OTPService.generate_otp()

        now = timezone.now()

        otp_object = EmailOTP.objects.create(
            email=email,
            otp=otp,
            purpose=purpose,
            expires_at=now + timedelta(
                minutes=OTP_EXPIRY_MINUTES
            )
        )

        return otp_object

    # verify the  latest OTP for the given email and purpose
    @staticmethod
    def verify_otp(
        email,
        otp,
        purpose
    ):

        email = email.lower().strip()

        otp_object = (
            EmailOTP.objects
            .filter(
                email=email,
                purpose=purpose,
                is_verified=False
            )
            .order_by("-created_at")
            .first()
        )

        if not otp_object:
            raise ValidationError(
                "Invalid or expired OTP."
            )

        if timezone.now() > otp_object.expires_at:

            otp_object.is_verified = True

            otp_object.save(
                update_fields=["is_verified"]
            )

            raise ValidationError(
                "OTP has expired."
            )

        if otp_object.attempts >= MAX_OTP_ATTEMPTS:

            otp_object.is_verified = True

            otp_object.save(
                update_fields=["is_verified"]
            )

            raise ValidationError(
                "Maximum OTP attempts exceeded."
            )

        if otp_object.otp != otp:

            otp_object.attempts += 1

            otp_object.save(
                update_fields=["attempts"]
            )

            raise ValidationError(
                "Invalid OTP."
            )

        otp_object.is_verified = True

        otp_object.save(
            update_fields=["is_verified"]
        )

        return True