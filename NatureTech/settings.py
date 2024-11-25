"""
Django settings for NatureTech project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

# Import the passwords file from passwords.json
import json
import os
from email.policy import default
from pathlib import Path
from unittest.mock import DEFAULT

with open("passwords.json") as f:
    passwords = json.load(f)
    django_password = passwords["django"]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = Path(__file__).resolve().parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = django_password["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["boer.butrosgroot.com", "boer-admin.butrosgroot.com"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_hosts",
    "booking_system",
    "customer_general",
    "authentication",
    "admin_general",
]

MIDDLEWARE = [
    "django_hosts.middleware.HostsRequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_hosts.middleware.HostsResponseMiddleware",
]

LOGIN_URL = "login"

AUTHENTICATION_BACKENDS = [
    "authentication.auth_backend.EmailOrUsernameModelBackend",
    "django.contrib.auth.backends.ModelBackend",
]

ROOT_HOSTCONF = "NatureTech.hosts"
ROOT_URLCONF = "NatureTech.boer_urls"
DEFAULT_HOST = "boer"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "debug": DEBUG,
        },
    },
]

WSGI_APPLICATION = "NatureTech.wsgi.application"

ASGI_APPLICATION = "NatureTech.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
            "capacity": 1500,  # default 100
            "expiry": 10,  # default 60
        },
    },
}


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "NatureTech",
        "USER": django_password["Database"]["user"],
        "PASSWORD": django_password["Database"]["password"],
        "HOST": django_password["Database"]["host"],  # Replace with the actual hostname
        "PORT": django_password["Database"][
            "port"
        ],  # Replace with the actual port number
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 6,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "GMT"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = "static/"
STATICFILES_DIRS = ["static_workfile/"]

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, "templates"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = django_password["email"]["host"]
EMAIL_USE_TLS = True
EMAIL_PORT = django_password["email"]["port"]
EMAIL_HOST_USER = django_password["email"]["user"]
EMAIL_HOST_PASSWORD = django_password["email"]["password"]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"
