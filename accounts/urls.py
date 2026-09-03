from django.urls import path

from .views import (
    RegisterView,
    VerifyRegistrationOTPView,
    ResendRegistrationOTPView,
    LoginView,
    ForgotPasswordOTPView,
    ForgotPasswordView,
    ChangePasswordOTPView,
    ChangePasswordView,
    ProfileView,
    UpdateProfileView,
    LogoutView,
)


urlpatterns = [

    # Register
    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),

    path(
        "register/verify-otp/",
        VerifyRegistrationOTPView.as_view(),
        name="verify-registration-otp"
    ),

    path(
        "register/resend-otp/",
        ResendRegistrationOTPView.as_view(),
        name="resend-registration-otp"
    ),

    # Login
    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

    # Forgot password
    path(
        "forgot-password/send-otp/",
        ForgotPasswordOTPView.as_view(),
        name="forgot-password-send-otp"
    ),

    path(
        "forgot-password/",
        ForgotPasswordView.as_view(),
        name="forgot-password"
    ),

    # Change password
    path(
        "change-password/send-otp/",
        ChangePasswordOTPView.as_view(),
        name="change-password-send-otp"
    ),

    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password"
    ),

    # Profile
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile"
    ),

    path(
        "profile/update/",
        UpdateProfileView.as_view(),
        name="profile-update"
    ),

    # Logout
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    ),
]