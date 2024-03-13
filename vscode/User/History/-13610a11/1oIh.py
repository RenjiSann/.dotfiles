from .auth import *
from .common import *  # noqa

SECRET_KEY = "CHANGE_ME"
DEBUG = True

# django-debug-toolbar

INSTALLED_APPS.append("debug_toolbar")

# needs to be as early as possible
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#add-the-middleware
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "gccsite.settings.debug.show_toolbar",
    "TOOLBAR_LANGUAGE": "en-us",
}
