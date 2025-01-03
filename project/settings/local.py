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
    "silk",
    "drf_spectacular",
    "custom_commands",
    "users",
    "movies",
    "finance",
]

MIDDLEWARE += [
    "silk.middleware.SilkyMiddleware",
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
    "TITLE": "Netflix clone",
    "DESCRIPTION": "This is a practice project on django",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": "/api/",
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
'''
# AWS Credentials

AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env.str("AWS_REGION")
AWS_S3_ENDPOINT_URL = env.str("AWS_S3_ENDPOINT_URL")
# Default File Storage
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
AWS_DEFAULT_ACL = (
    "public-read"  # Set file permissions (public-read or private)
)
AWS_QUERYSTRING_AUTH = False  # Disable querystring authentication
AWS_S3_FILE_OVERWRITE = (
    False  # Prevent overwriting existing files with the same name
)
AWS_LOCATION = "media"

MEDIA_URL = (
    f"http://s3.ap-southeast-1.wasabisys.com/{AWS_STORAGE_BUCKET_NAME}/"
)
'''
# STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/static/'
'''
AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env.str("AWS_REGION")
AWS_S3_CUSTOM_DOMAIN = env.str("AWS_S3_ENDPOINT_URL")
# Static files settings
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Media files settings
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# STORAGES configuration
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        #"OPTIONS": {
         #   "access_key": AWS_ACCESS_KEY_ID,
          #  "secret_key": AWS_SECRET_ACCESS_KEY,
           # "bucket_name": AWS_STORAGE_BUCKET_NAME,
            #"region_name": AWS_S3_REGION_NAME,
            #"custom_domain": AWS_S3_CUSTOM_DOMAIN,
            #"file_overwrite": False,  # Optional
        #}
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        #"OPTIONS": {
         #   "access_key": AWS_ACCESS_KEY_ID,
          #  "secret_key": AWS_SECRET_ACCESS_KEY,
           # "bucket_name": AWS_STORAGE_BUCKET_NAME,
            #"region_name": AWS_S3_REGION_NAME,
            #"custom_domain": AWS_S3_CUSTOM_DOMAIN,
            #"file_overwrite": False,  # Optional
        #},
    },
}
'''