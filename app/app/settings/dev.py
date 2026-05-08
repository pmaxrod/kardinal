from .base import *
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG")
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

# Database PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE"),
        "NAME": os.environ.get("SQL_DATABASE_NAME"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
ALLOWED_HOSTS = []

if DEBUG:
    INSTALLED_APPS += ["django_browser_reload"]
    MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]

try:
    from .local import *
except ImportError:
    pass
