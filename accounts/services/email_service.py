from django.conf import settings
from django.core.mail import send_mail


class EmailService:

    @staticmethod
    def send_otp_email(
        email,
        otp,
        purpose
    ):

        if purpose == "registration":

            subject = "Verify Your Email"

        elif purpose == "forgot_password":

            subject = "Reset Password OTP"

        elif purpose == "change_password":

            subject = "Change Password OTP"

        else:

            subject = "Your Verification OTP"

        message = f"""
Hello,

Your OTP is:

{otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.

Regards,
Your Application Team
"""

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

    @staticmethod
    def send_welcome_email(
        email,
        first_name
    ):

        send_mail(
            subject="Welcome",
            message=(
                f"Hello {first_name},\n\n"
                "Your account has been successfully verified."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )