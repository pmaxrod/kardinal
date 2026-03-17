from .base import *

DEBUG = False

# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/6.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

TAILWIND_CLI_VERSION = '4.2.1'
TAILWIND_CLI_AUTOMATIC_DOWNLOAD = False
TAILWIND_CLI_PATH = '/usr/local/bin/tailwindcss'

try:
    from .local import *
except ImportError:
    pass
