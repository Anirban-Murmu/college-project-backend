from pathlib import Path
from decouple import config
from datetime import timedelta


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = config("SECRET_KEY")
DEBUG = config(
    "DEBUG",
    default=False,
    cast=bool,
)


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "corsheaders",
    "cloudinary",
    "cloudinary_storage",

    # Local apps
    "accounts.apps.AccountsConfig",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL / WSGI
# ============================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]




# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ============================================================
# MEDIA
# ============================================================

# MEDIA_URL = "/media/"

# MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# ClOUDINARY sTORAGE
# ============================================================
# CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME")
# CLOUDINARY_API_KEY = config("CLOUDINARY_API_KEY")
# CLOUDINARY_API_SECRET = config("CLOUDINARY_API_SECRET")


CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": config("CLOUDINARY_API_KEY"),
    "API_SECRET": config("CLOUDINARY_API_SECRET"),
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# CUSTOM USER MODEL
# ============================================================

AUTH_USER_MODEL = "accounts.User"


# ============================================================
# EMAIL
# ============================================================

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "OPTIONS": {
            "host": config("EMAIL_HOST"),
            "port": config("EMAIL_PORT", cast=int),
            "username": config("EMAIL_HOST_USER"),
            "password": config("EMAIL_HOST_PASSWORD"),
            "use_tls": config("EMAIL_USE_TLS", cast=bool),
            "timeout": 10,
        },
    },
}

DEFAULT_FROM_EMAIL = config("EMAIL_HOST_USER")


# ============================================================
# DJANGO REST FRAMEWORK
# ============================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],

    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],

    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",

    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],

    "DEFAULT_THROTTLE_RATES": {
        "anon": "20/minute",
        "user": "100/minute",

        "login": "5/minute",
        "register": "3/minute",

        "registration_otp": "3/minute",
        "registration_otp_verify": "5/minute",

        "forgot_password": "3/minute",
        "forgot_password_otp": "3/minute",

        "change_password": "5/minute",
        "change_password_otp": "3/minute",
    },
}


# ============================================================
# SIMPLE JWT
# ============================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config(
            "JWT_ACCESS_TOKEN_MINUTES",
            default=30,
            cast=int,
        )
    ),

    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config(
            "JWT_REFRESH_TOKEN_DAYS",
            default=7,
            cast=int,
        )
    ),

    "ROTATE_REFRESH_TOKENS": True,

    "BLACKLIST_AFTER_ROTATION": True,

    "UPDATE_LAST_LOGIN": True,

    "AUTH_HEADER_TYPES": ("Bearer",),
}


# ============================================================
# DRF SPECTACULAR
# ============================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "College Project API",

    "DESCRIPTION": (
        "Authentication and user management API "
        "built with Django REST Framework."
    ),

    "VERSION": "1.0.0",

    "SERVE_INCLUDE_SCHEMA": False,

    "TAGS": [
        {
            "name": "Authentication",
            "description": (
                "Register, login, OTP and JWT authentication"
            ),
        },
        {
            "name": "Password",
            "description": (
                "Forgot and change password operations"
            ),
        },
        {
            "name": "Profile",
            "description": "User profile operations",
        },
        {
            "name": "Logout",
            "description": "JWT logout operations",
        },
    ],
}


# ============================================================
# FIREBASE
# ============================================================

FIREBASE_PROJECT_ID = config("FIREBASE_PROJECT_ID")
FIREBASE_PRIVATE_KEY_ID = config("FIREBASE_PRIVATE_KEY_ID")
FIREBASE_PRIVATE_KEY = config("FIREBASE_PRIVATE_KEY").replace("\\n", "\n")
FIREBASE_CLIENT_EMAIL = config("FIREBASE_CLIENT_EMAIL")
FIREBASE_CLIENT_ID = config("FIREBASE_CLIENT_ID")
FIREBASE_DATABASE_URL = config("FIREBASE_DATABASE_URL")



