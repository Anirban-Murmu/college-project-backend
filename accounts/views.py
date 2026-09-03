
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework import status

from drf_spectacular.utils import extend_schema

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    VerifyRegistrationOTPSerializer,
    ResendRegistrationOTPSerializer,
    ForgotPasswordOTPSerializer,
    ForgotPasswordSerializer,
    ChangePasswordOTPSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
    LogoutSerializer,
)


from .throttles import (
    LoginThrottle,
    RegisterThrottle,
    RegistrationOTPThrottle,
    RegistrationOTPVerifyThrottle,
    ForgotPasswordThrottle,
    ForgotPasswordOTPThrottle,
    ChangePasswordThrottle,
    ChangePasswordOTPThrottle,
    NormalUserThrottle,
)


# ============================================================
# REGISTER
# ============================================================

class RegisterView(APIView):

    permission_classes = [AllowAny]
    throttle_classes = [RegisterThrottle]

    @extend_schema(
        tags=["Authentication"],
        request=RegisterSerializer,
        responses={
            201: RegisterSerializer,
            400: {
                "description": "Validation error"
            },
        },
        summary="Register a new user",
        description=(
            "Creates a new user account and sends "
            "a 6-digit OTP to the user's email."
        ),
    )
    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": (
                    "Registration successful. "
                    "Please verify your email with the OTP."
                )
            },
            status=status.HTTP_201_CREATED
        )


# ============================================================
# VERIFY REGISTRATION OTP
# ============================================================

class VerifyRegistrationOTPView(APIView):

    permission_classes = [AllowAny]
    throttle_classes = [RegistrationOTPVerifyThrottle]

    @extend_schema(
        tags=["Authentication"],
        request=VerifyRegistrationOTPSerializer,
        responses={
            200: {
                "description": "Email verified successfully."
            },
            400: {
                "description": "Invalid or expired OTP."
            },
        },
        summary="Verify registration OTP",
        description=(
            "Verifies the 6-digit OTP sent to the user's "
            "email during registration."
        ),
    )
    def post(self, request):

        serializer = VerifyRegistrationOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message":
                    "Email verified successfully."
            },
            status=status.HTTP_200_OK
        )


# ============================================================
# RESEND REGISTRATION OTP
# ============================================================

class ResendRegistrationOTPView(APIView):

    permission_classes = [AllowAny]
    throttle_classes = [RegistrationOTPThrottle]

    @extend_schema(
        tags=["Authentication"],
        request=ResendRegistrationOTPSerializer,
        responses={
            200: {
                "description": "OTP resent successfully."
            },
            400: {
                "description": "Validation error."
            },
        },
        summary="Resend registration OTP",
        description=(
            "Generates a new 6-digit OTP and sends it "
            "to the user's email."
        ),
    )
    def post(self, request):

        serializer = ResendRegistrationOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = serializer.save()

        return Response(
            result,
            status=status.HTTP_200_OK
        )


# ============================================================
# LOGIN
# ============================================================

class LoginView(APIView):

    permission_classes = [AllowAny]
    throttle_classes = [LoginThrottle]

    @extend_schema(
        tags=["Authentication"],
        request=LoginSerializer,
        responses={
            200: {
                "description": "Login successful. Returns JWT tokens."
            },
            400: {
                "description": "Invalid email or password."
            },
        },
        summary="Login",
        description=(
            "Authenticates the user using email and password "
            "and returns access and refresh JWT tokens."
        ),
    )
    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        tokens = serializer.save()

        return Response(
            {
                "message":
                    "Login successful.",
                "tokens":
                    tokens,
            },
            status=status.HTTP_200_OK
        )


# ============================================================
# FORGOT PASSWORD - SEND OTP
# ============================================================

class ForgotPasswordOTPView(APIView):

    permission_classes = [AllowAny]
    throttle_classes = [ForgotPasswordOTPThrottle]


    @extend_schema(
        tags=["Password"],
        request=ForgotPasswordOTPSerializer,
        responses={
            200: {
                "description": "Password reset OTP sent successfully."
            },
            400: {
                "description": "Validation error."
            },
        },
        summary="Send forgot-password OTP",
        description=(
            "Sends a 6-digit OTP to the user's email "
            "for password reset."
        ),
    )
    def post(self, request):

        serializer = ForgotPasswordOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = serializer.save()

        return Response(
            result,
            status=status.HTTP_200_OK
        )


# ============================================================
# FORGOT PASSWORD - RESET
# ============================================================

class ForgotPasswordView(APIView):

    permission_classes = [AllowAny]
    throttle_classes = [ForgotPasswordThrottle]

    @extend_schema(
        tags=["Password"],
        request=ForgotPasswordSerializer,
        responses={
            200: {
                "description": "Password reset successfully."
            },
            400: {
                "description": "Invalid OTP or password."
            },
        },
        summary="Reset forgotten password",
        description=(
            "Resets the user's password after successful "
            "OTP verification."
        ),
    )
    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message":
                    "Password reset successfully."
            },
            status=status.HTTP_200_OK
        )


# ============================================================
# CHANGE PASSWORD - SEND OTP
# ============================================================

class ChangePasswordOTPView(APIView):

    permission_classes = [IsAuthenticated]
    throttle_classes = [ChangePasswordOTPThrottle]

    @extend_schema(
        tags=["Password"],
        request=ChangePasswordOTPSerializer,
        responses={
            200: {
                "description": "Change-password OTP sent successfully."
            },
            401: {
                "description": "Authentication required."
            },
        },
        summary="Send change-password OTP",
        description=(
            "Sends a 6-digit OTP to the authenticated "
            "user's email."
        ),
    )
    def post(self, request):

        serializer = ChangePasswordOTPSerializer(
            data=request.data,
            context={
                "request": request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = serializer.save()

        return Response(
            result,
            status=status.HTTP_200_OK
        )


# ============================================================
# CHANGE PASSWORD
# ============================================================

class ChangePasswordView(APIView):

    permission_classes = [ IsAuthenticated]
    throttle_classes = [ChangePasswordThrottle]

    @extend_schema(
        tags=["Password"],
        request=ChangePasswordSerializer,
        responses={
            200: {
                "description": "Password changed successfully."
            },
            400: {
                "description": "Invalid old password, OTP, or new password."
            },
            401: {
                "description": "Authentication required."
            },
        },
        summary="Change password",
        description=(
            "Changes the authenticated user's password "
            "after verifying the old password and OTP."
        ),
    )
    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={
                "request": request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = serializer.save()

        return Response(
            result,
            status=status.HTTP_200_OK
        )


# ============================================================
# PROFILE
# ============================================================

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]
    throttle_classes = [NormalUserThrottle]


    @extend_schema(
        tags=["Profile"],
        responses={
            200: ProfileSerializer,
            401: {
                "description": "Authentication required."
            },
        },
        summary="Get user profile",
        description=(
            "Returns the profile information of "
            "the authenticated user."
        ),
    )
    def get(self, request):

        serializer = ProfileSerializer(
            request.user,
            context={
                "request": request
            }
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


# ============================================================
# UPDATE PROFILE
# ============================================================

class UpdateProfileView(APIView):

    permission_classes = [IsAuthenticated]
    throttle_classes = [NormalUserThrottle]


    @extend_schema(
        tags=["Profile"],
        request=UpdateProfileSerializer,
        responses={
            200: UpdateProfileSerializer,
            400: {
                "description": "Validation error."
            },
            401: {
                "description": "Authentication required."
            },
        },
        summary="Update user profile",
        description=(
            "Updates the authenticated user's profile "
            "information."
        ),
    )
    def patch(self, request):

        serializer = UpdateProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={
                "request": request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message":
                    "Profile updated successfully.",
                "data":
                    serializer.data,
            },
            status=status.HTTP_200_OK
        )


# ============================================================
# LOGOUT
# ============================================================

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]
    throttle_classes = [NormalUserThrottle]


    @extend_schema(
        tags=["Logout"],
        request=LogoutSerializer,
        responses={
            200: {
                "description": "Logout successful."
            },
            400: {
                "description": "Invalid refresh token."
            },
            401: {
                "description": "Authentication required."
            },
        },
        summary="Logout",
        description=(
            "Blacklists the refresh JWT token and "
            "logs the user out."
        ),
    )
    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = serializer.save()

        return Response(
            result,
            status=status.HTTP_200_OK
        )

