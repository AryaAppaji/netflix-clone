from .base import *
from django.core.management.utils import get_random_secret_key
import environ
import os

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

TIME_ZONE = env.str("TIME_ZONE", "Asia/Kolkata")
SECRET_KEY = env.str("DJANGO_SECRET_KEY", get_random_secret_key())
DEBUG = env.bool("DJANGO_DEBUG", True)
AUTH_USER_MODEL = "users.CustomUser"

INSTALLED_APPS += [
    "storages",
    "rest_framework",
    "rest_framework.authtoken",
    "django_sonar",
    "drf_spectacular",
    "custom_commands",
    "users",
    "movies",
    "finance",
]

MIDDLEWARE += [
    "django_sonar.middlewares.requests.RequestsMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE", default="django.db.backends.postgresql"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "media/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{name} {levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",  # Capture all logs from DEBUG and above
            "class": "logging.FileHandler",
            "filename": "django.log",
            "formatter": "verbose",  # Use the detailed formatter
        },
    },
    "root": {
        "handlers": ["file"],  # Attach the file handler to capture all logs
        "level": "DEBUG",  # Capture all logs starting from DEBUG
    },
    "loggers": {
        "django": {
            "handlers": [
                "file"
            ],  # Attach the file handler for Django-specific logs
            "level": "DEBUG",  # Capture all logs starting from DEBUG
            "propagate": True,
        },
    },
}


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Netfilix Clone",
    "DESCRIPTION": "This is a practice project on django",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": True,
    "SECURITY": [
        {"bearerAuth": []}
    ],  # Specifies the use of Bearer token for authentication
    "COMPONENTS": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",  # Uses the Bearer authentication scheme
                "bearerFormat": "",  # No need for JWT format here
            },
        },
    },
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")

APPEND_SLASH = True

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "media/"

DJANGO_SONAR = {
    "excludes": [
        MEDIA_URL,
        "/sonar/",
        "/admin/",
        "/__reload__/",
    ],
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # Replace this with your redis location.
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
