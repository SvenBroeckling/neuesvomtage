# -*- coding: utf-8 -*-
import os

from django.contrib import messages
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, ".env"))

BASE_URL = os.environ["BASE_URL"]
SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = True if os.environ["DEBUG"] == "True" else False
ADMINS = (("Sven Bröckling", "sven@broeckling.de"),)
MANAGERS = ADMINS

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")
CSRF_TRUSTED_ORIGINS = [f"https://{a}" for a in ALLOWED_HOSTS]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Language / i18n
_ = lambda x: x

USE_I18N = True
USE_L10N = True
TIME_ZONE = "Europe/Berlin"
LANGUAGE_CODE = "de"
LANGUAGES = (
    ("de", _("German")),
    ("en", _("English")),
)

SESSION_COOKIE_AGE = 60 * 60 * 24 * 365  # 1 year


# Media
MEDIA_ROOT = os.path.join(BASE_DIR, "media_files")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "static_files")
STATIC_URL = "/static/"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

# Setup support for proxy headers
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

COMPRESS_ENABLED = True
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

if os.environ.get("DATABASE_ENGINE", None) is None:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.environ["DATABASE_ENGINE"],
            "NAME": os.environ["DATABASE_NAME"],
            "USER": os.environ["DATABASE_USER"],
            "PASSWORD": os.environ["DATABASE_PASSWORD"],
            "HOST": os.environ["DATABASE_HOST"],
            "PORT": int(os.environ["DATABASE_PORT"]),
        }
    }

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.media",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "base.context_processors.theme",
            ],
        },
    },
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

ROOT_URLCONF = "neuesvomtage.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.admin",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "compressor",
    "django_bootstrap5",
    "sorl.thumbnail",
    "django_extensions",
    "cachalot",
    "base",
    "quiz",
]

MESSAGE_TAGS = {messages.ERROR: "danger"}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "mail_admins": {"level": "ERROR", "class": "django.utils.log.AdminEmailHandler"}
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

SILENCED_SYSTEM_CHECKS = [
    "cachalot.W001",
    "cachalot.W002",
]  # cachalot complaining about wrong redis cache, but uses it
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}",
        "KEY_PREFIX": "neuesvomtage_cache",
    }
}
