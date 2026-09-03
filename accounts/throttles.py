from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle


class LoginThrottle(AnonRateThrottle):
    scope = "login"


class RegisterThrottle(AnonRateThrottle):
    scope = "register"


class RegistrationOTPThrottle(AnonRateThrottle):
    scope = "registration_otp"


class RegistrationOTPVerifyThrottle(AnonRateThrottle):
    scope = "registration_otp_verify"


class ForgotPasswordThrottle(AnonRateThrottle):
    scope = "forgot_password"


class ForgotPasswordOTPThrottle(AnonRateThrottle):
    scope = "forgot_password_otp"


class ChangePasswordThrottle(UserRateThrottle):
    scope = "change_password"


class ChangePasswordOTPThrottle(UserRateThrottle):
    scope = "change_password_otp"


class NormalUserThrottle(UserRateThrottle):
    scope = "user"