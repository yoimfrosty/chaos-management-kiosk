"""
Django settings for OceanCityKiosk project.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-d-^_1oqbl)#27c5*wx5-0q#1$y2rrn%i+ddysr8k7#acg29pei"
)

# Use DEBUG=True only when environment variable says True
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "testserver",
    ".ondigitalocean.app",
    "whale-app-pcttw.ondigitalocean.app",
    "canna-pharmskiosk.com",
    "www.canna-pharmskiosk.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.ondigitalocean.app",
    "https://whale-app-pcttw.ondigitalocean.app",
    "https://canna-pharmskiosk.com",
    "https://www.canna-pharmskiosk.com",
]

# If you want to allow all hosts while testing, uncomment this:
# ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "kiosk.apps.KioskConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "OceanCityKiosk.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "OceanCityKiosk.wsgi.application"


# Database
# Local development uses SQLite if DATABASE_URL does not exist.
# DigitalOcean PostgreSQL uses DATABASE_URL automatically.
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=bool(os.getenv("DATABASE_URL")),
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"


# CSRF trusted origins for DigitalOcean
CSRF_TRUSTED_ORIGINS = [
    "https://*.ondigitalocean.app",
    "https://whale-app-pcttw.ondigitalocean.app",
]


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"