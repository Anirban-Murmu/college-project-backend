from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from accounts.models import User
from accounts.services.otp_service import OTPService


class PasswordService:

    @staticmethod
    def reset_password(
        email,
        otp,
        new_password
    ):

        user = User.objects.filter(
            email=email
        ).first()

        if not user:
            raise ValidationError(
                "User not found."
            )

        OTPService.verify_otp(
            email=email,
            otp=otp,
            purpose="forgot_password"
        )

        validate_password(
            new_password,
            user
        )

        user.set_password(
            new_password
        )

        user.save(
            update_fields=["password"]
        )

        return user

    @staticmethod
    def change_password(
        user,
        old_password,
        otp,
        new_password
    ):

        if not user.check_password(
            old_password
        ):
            raise ValidationError(
                "Old password is incorrect."
            )

        OTPService.verify_otp(
            email=user.email,
            otp=otp,
            purpose="change_password"
        )

        validate_password(
            new_password,
            user
        )

        user.set_password(
            new_password
        )

        user.save(
            update_fields=["password"]
        )

        return user