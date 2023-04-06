"""
Django settings for governanceplatform project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import importlib
import os
import sys

try:
    from governanceplatform import config  # type: ignore
except ImportError:  # pragma: no cover
    from governanceplatform import config_dev as config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

try:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = config.SECRET_KEY
    HASH_KEY = config.HASH_KEY

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = config.DEBUG
    LOGGING = config.LOGGING
    LOG_DIRECTORY = config.LOG_DIRECTORY


    ALLOWED_HOSTS = config.ALLOWED_HOSTS
    PUBLIC_URL = config.PUBLIC_URL
    OPERATOR_CONTACT = config.OPERATOR_CONTACT

    EMAIL_HOST = config.EMAIL_HOST
    EMAIL_PORT = config.EMAIL_PORT
except AttributeError as e:
    print("Please check you configuration file for the missing configuration variable:")
    print(f"  {e}")
    exit(1)

try:
    CORS_ALLOWED_ORIGINS = config.CORS_ALLOWED_ORIGINS
    CORS_ALLOWED_ORIGIN_REGEXES = config.CORS_ALLOWED_ORIGIN_REGEXES
    CORS_ALLOW_METHODS = config.CORS_ALLOW_METHODS
except AttributeError:
    CORS_ALLOWED_ORIGINS = []
    CORS_ALLOWED_ORIGIN_REGEXES = []
    CORS_ALLOW_METHODS = []

try:
    if LOG_DIRECTORY:
        # if not logging in stdout
        os.makedirs(LOG_DIRECTORY, exist_ok=True)
except Exception as e:
    print("Impossible to create the log directory:")
    print(f"  {e}")
    exit(1)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
    'regulator',
    'operateur',
    "drf_spectacular",
    "drf_spectacular_sidecar",  # required for Django collectstatic discovery
    "corsheaders",
]

context_processors = [
    "django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "survey.context_processors.get_version",
    "survey.context_processors.instance_configurations",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.locale.LocaleMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    context_processors.append("django.template.context_processors.debug")
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


ROOT_URLCONF = "governanceplatform.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            'templates'
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": context_processors,
        },
    },
]

WSGI_APPLICATION = 'governanceplatform.wsgi.application'


DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

STATIC_DIR = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = [
    STATIC_DIR,
]

# Used to get an access to the header on JS side.
CORS_EXPOSE_HEADERS = [
    "content-disposition",
]


