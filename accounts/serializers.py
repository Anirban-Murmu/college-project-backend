from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from .validators import (
    validate_name,
    validate_passwords,
    validate_email_password,
    validate_password_change,
    validate_password_reset_email_link,
    validate_otp,
)

from .services import (
    OTPService,
    EmailService,
    PasswordService,
    get_tokens_for_user,
    get_profile_image,
)


User = get_user_model()

from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Register Example",
            value={
                "first_name": "John",
                "middle_name": "David",
                "last_name": "Doe",
                "email": "john@example.com",
                "password": "Password@123",
                "password2": "Password@123",
                "tc": True,
            },
            request_only=True,
        )
    ]
)




# ============================================================
# REGISTER
# ============================================================

class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "image",
            "gender",
            "password",
            "password2",
            "tc",
        ]

        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": True,
            }
        }

    def validate_first_name(self, value):
        validate_name(value)
        return value

    def validate_middle_name(self, value):

        if value:
            validate_name(value)

        return value

    def validate_last_name(self, value):
        validate_name(value)
        return value

    def validate_email(self, value):

        value = value.lower().strip()

        if User.objects.filter(
            email__iexact=value
        ).exists():

            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def validate_password(self, value):

        validate_password(value)

        return value

    def validate(self, attrs):

        validate_passwords(attrs)

        if not attrs.get("tc"):

            raise serializers.ValidationError({
                "tc":
                    "You must accept Terms and Conditions."
            })

        return attrs

    def create(self, validated_data):

        validated_data.pop("password2")

        user = User.objects.create_user(
        **validated_data
        )

        user.is_active = False

        user.save(update_fields=["is_active"])
        return user

       # return User.objects.create_user(  **validated_data )


# ============================================================
# LOGIN
# ============================================================

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=True
    )

    password = serializers.CharField(
        write_only=True,
        required=True
    )

    def validate(self, attrs):

        validate_email_password(attrs)

        email = attrs["email"].lower().strip()
        password = attrs["password"]

        user = User.objects.filter(
            email__iexact=email
        ).first()

        if not user:
            raise serializers.ValidationError({
                "error":
                    "Invalid email or password."
            })

        if not user.check_password(password):
            raise serializers.ValidationError({
                "error":
                    "Invalid email or password."
            })

        if not user.is_active:
            raise serializers.ValidationError({
                "error":
                    "User is not active."
            })

        attrs["user"] = user

        return attrs

    def create(self, validated_data):

        return get_tokens_for_user(
            validated_data["user"]
        )


# ============================================================
# REGISTRATION - VERIFY OTP
# ============================================================

class VerifyRegistrationOTPSerializer(
    serializers.Serializer
):

    email = serializers.EmailField(
        required=True
    )

    otp = serializers.CharField(
        required=True,
        min_length=6,
        max_length=6
    )

    def validate(self, attrs):

        validate_otp(attrs)

        attrs["email"] = (
            attrs["email"]
            .lower()
            .strip()
        )

        return attrs

    def save(self):

        email = self.validated_data["email"]
        otp = self.validated_data["otp"]

        OTPService.verify_otp(
            email=email,
            otp=otp,
            purpose="registration"
        )

        user = User.objects.filter(
            email__iexact=email
        ).first()

        if not user:

            raise serializers.ValidationError({
                "error":
                    "User does not exist."
            })

        user.is_active = True

        user.save(
            update_fields=["is_active"]
        )

        return user


# ============================================================
# RESEND REGISTRATION OTP
# ============================================================

class ResendRegistrationOTPSerializer(
    serializers.Serializer
):

    email = serializers.EmailField(
        required=True
    )

    def validate_email(self, value):

        value = value.lower().strip()

        if not User.objects.filter(
            email__iexact=value
        ).exists():

            raise serializers.ValidationError({
                "email":
                    "User does not exist."
            })

        return value

    def save(self):

        email = self.validated_data["email"]

        otp_object = OTPService.create_otp(
            email=email,
            purpose="registration"
        )

        EmailService.send_otp_email(
            email=email,
            otp=otp_object.otp,
            purpose="registration"
        )

        return {
            "message":
                "OTP sent successfully."
        }


# ============================================================
# FORGOT PASSWORD - SEND OTP
# ============================================================

class ForgotPasswordOTPSerializer(
    serializers.Serializer
):

    email = serializers.EmailField(
        required=True
    )

    def validate(self, attrs):

        validate_password_reset_email_link(
            attrs
        )

        attrs["email"] = (
            attrs["email"]
            .lower()
            .strip()
        )

        if not User.objects.filter(
            email__iexact=attrs["email"]
        ).exists():

            raise serializers.ValidationError({
                "email":
                    "User with this email does not exist."
            })

        return attrs

    def save(self):

        email = self.validated_data["email"]

        otp_object = OTPService.create_otp(
            email=email,
            purpose="forgot_password"
        )

        EmailService.send_otp_email(
            email=email,
            otp=otp_object.otp,
            purpose="forgot_password"
        )

        return {
            "message":
                "Password reset OTP sent successfully."
        }


# ============================================================
# FORGOT PASSWORD - RESET
# ============================================================

class ForgotPasswordSerializer(
    serializers.Serializer
):

    email = serializers.EmailField(
        required=True
    )

    otp = serializers.CharField(
        required=True,
        min_length=6,
        max_length=6
    )

    password = serializers.CharField(
        write_only=True,
        required=True
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    def validate_password(self, value):

        validate_password(value)

        return value

    def validate(self, attrs):

        validate_passwords(attrs)
        validate_otp(attrs)

        attrs["email"] = (
            attrs["email"]
            .lower()
            .strip()
        )

        return attrs

    def save(self):

        return PasswordService.reset_password(
            email=self.validated_data["email"],
            otp=self.validated_data["otp"],
            new_password=self.validated_data["password"]
        )


# ============================================================
# CHANGE PASSWORD - SEND OTP
# ============================================================

class ChangePasswordOTPSerializer(
    serializers.Serializer
):

    def save(self):

        user = self.context[
            "request"
        ].user

        otp_object = OTPService.create_otp(
            email=user.email,
            purpose="change_password"
        )

        EmailService.send_otp_email(
            email=user.email,
            otp=otp_object.otp,
            purpose="change_password"
        )

        return {
            "message":
                "Password change OTP sent successfully."
        }


# ============================================================
# CHANGE PASSWORD
# ============================================================

class ChangePasswordSerializer(
    serializers.Serializer
):

    old_password = serializers.CharField(
        write_only=True,
        required=True
    )

    otp = serializers.CharField(
        required=True,
        min_length=6,
        max_length=6
    )

    password = serializers.CharField(
        write_only=True,
        required=True
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    def validate_password(self, value):

        user = self.context[
            "request"
        ].user

        validate_password(
            value,
            user
        )

        return value

    def validate(self, attrs):

        validate_password_change(attrs)
        validate_otp(attrs)

        return attrs

    def save(self):

        user = self.context[
            "request"
        ].user

        PasswordService.change_password(
            user=user,
            old_password=self.validated_data[
                "old_password"
            ],
            otp=self.validated_data["otp"],
            new_password=self.validated_data[
                "password"
            ]
        )

        return {
            "message":
                "Password changed successfully."
        }


# ============================================================
# PROFILE
# ============================================================

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
            "image",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "gender",
        ]

        read_only_fields = [
            "id",
            "email",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if request:
            data["image"] = get_profile_image(
                instance,
                request
            )

        return data

# ============================================================
# UPDATE PROFILE
# ============================================================

class UpdateProfileSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = User

        fields = [
            "image",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
        ]

    def validate_first_name(self, value):

        validate_name(value)

        return value

    def validate_middle_name(self, value):

        if value:
            validate_name(value)

        return value

    def validate_last_name(self, value):

        validate_name(value)

        return value

    def to_representation(self, instance):

        data = super().to_representation(instance)

        request = self.context.get("request")

        if request:
            data["image"] = get_profile_image(
                instance,
                request
            )

        return data
# ============================================================
# LOGOUT
# ============================================================

class LogoutSerializer(
    serializers.Serializer
):

    refresh = serializers.CharField(
        required=True
    )

    def save(self):

        from rest_framework_simplejwt.tokens import (
            RefreshToken
        )

        try:

            token = RefreshToken(
                self.validated_data["refresh"]
            )

            token.blacklist()

        except Exception:

            raise serializers.ValidationError({
                "refresh":
                    "Invalid or expired refresh token."
            })

        return {
            "message":
                "Logout successful."
        }