import re

from django.core.exceptions import ValidationError
from rest_framework import serializers


# ============================================================
# NAME VALIDATION
# ============================================================

def validate_name(value):
    """
    Name must:
    - Start with a capital letter
    - Contain only letters, spaces, hyphens, or apostrophes
    """

    if not value:
        raise ValidationError(
            "Name is required."
        )

    if not re.match(
        r"^[A-Z][A-Za-z' -]*$",
        value
    ):
        raise ValidationError(
            "Name must start with a capital letter."
        )


# ============================================================
# PASSWORD STRENGTH
# ============================================================

class StrongPasswordValidator:
    """
    Password must contain:
    - At least 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 number
    - At least 1 special character
    """

    def validate(self, password, user=None):

        if len(password) < 8:
            raise ValidationError(
                "Password must contain at least 8 characters."
            )

        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", password):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"[0-9]", password):
            raise ValidationError(
                "Password must contain at least one number."
            )

        if not re.search(
            r"[^A-Za-z0-9]",
            password
        ):
            raise ValidationError(
                "Password must contain at least one special character."
            )

    def get_help_text(self):

        return (
            "Password must contain at least 8 characters, "
            "one uppercase letter, one lowercase letter, "
            "one number, and one special character."
        )


# ============================================================
# PASSWORD + PASSWORD2
# ============================================================

def validate_passwords(attrs):

    password = attrs.get("password")
    password2 = attrs.get("password2")

    if password != password2:

        raise serializers.ValidationError({
            "password2":
                "Passwords do not match."
        })

    return attrs


# ============================================================
# EMAIL + PASSWORD
# ============================================================

def validate_email_password(attrs):

    email = attrs.get("email")
    password = attrs.get("password")

    if not email:

        raise serializers.ValidationError({
            "email":
                "Email is required."
        })

    if not password:

        raise serializers.ValidationError({
            "password":
                "Password is required."
        })

    return attrs


# ============================================================
# PASSWORD CHANGE
# ============================================================

def validate_password_change(attrs):

    password = attrs.get("password")
    password2 = attrs.get("password2")

    if not password:

        raise serializers.ValidationError({
            "password":
                "Password is required."
        })

    if not password2:

        raise serializers.ValidationError({
            "password2":
                "Confirm password is required."
        })

    if password != password2:

        raise serializers.ValidationError({
            "password2":
                "Passwords do not match."
        })

    return attrs


# ============================================================
# PASSWORD RESET EMAIL
# ============================================================

def validate_password_reset_email_link(attrs):

    email = attrs.get("email")

    if not email:

        raise serializers.ValidationError({
            "email":
                "Email is required."
        })

    return attrs


# ============================================================
# OTP VALIDATION
# ============================================================

def validate_otp(attrs):

    otp = attrs.get("otp")

    if not otp:

        raise serializers.ValidationError({
            "otp":
                "OTP is required."
        })

    if not otp.isdigit():

        raise serializers.ValidationError({
            "otp":
                "OTP must contain only numbers."
        })

    if len(otp) != 6:

        raise serializers.ValidationError({
            "otp":
                "OTP must be 6 digits."
        })

    return attrs