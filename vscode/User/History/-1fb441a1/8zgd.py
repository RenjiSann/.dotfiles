from os import path
from pathlib import Path

from gccsite import env

from .debug import DEBUG

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get_secret("DJANGO_SECRET_KEY")

PROBES_IPS = env.get_list("DJANGO_PROBES_IP", ["0.0.0.0/0"])
ALLOWED_HOSTS = env.get_list("DJANGO_ALLOWED_HOSTS", [])
DEFAULT_DOMAIN = ALLOWED_HOSTS[0] if ALLOWED_HOSTS else "app.localhost"
ALLOWED_CIDR_NETS = env.get_list("DJANGO_ALLOWED_CIDR", [])

# A list of the emails who get error notifications.
ADMINS = [(mail, mail) for mail in env.get_list("DJANGO_ADMINS", [])]
MANAGERS = [
    (mail, mail) for mail in env.get_list("DJANGO_MANAGERS", [])
] or ADMINS

# Redirect plain HTTP requests to HTTPS.
SECURE_SSL_REDIRECT = not DEBUG
SECURE_REDIRECT_EXEMPT = env.get_list(
    "DJANGO_SECURE_REDIRECT_EXEMPT", ["^metrics$"]
)

# Avoid transmitting the CSRF cookie over HTTP accidentally.
CSRF_COOKIE_SECURE = not DEBUG

# Avoid transmitting the session cookie over HTTP accidentally.
SESSION_COOKIE_SECURE = not DEBUG

# See https://docs.djangoproject.com/en/4.0/ref/middleware/#referrer-policy
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!

PROJECT_NAME = "gccsite"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mozilla_django_oidc",
    "django_celery_beat",
    "post_office",
    "crispy_forms",
    "crispy_bootstrap5",
    "events",
    "users",
    "pages",
    "partners",

    "phonenumber_field",
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

ROOT_URLCONF = "gccsite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "gccsite" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "gccsite.context_processors.my_context_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "gccsite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django_prometheus.db.backends.postgresql",
        "NAME": env.get_string("DB_NAME", "gccsite"),
        "USER": env.get_string("DB_USER", "gccsite"),
        "PASSWORD": env.get_secret("DB_PASSWORD"),
        "HOST": env.get_string("DB_HOST", "localhost"),
        "PORT": env.get_int("DB_PORT", 5432),
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
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# By default, bring back user to home when successfully logging in
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "users.User"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email settings

DEFAULT_FROM_EMAIL = env.get_string(
    "DJANGO_DEFAULT_FROM_EMAIL", f"noreply@{DEFAULT_DOMAIN}"
)

EMAIL_BACKEND = "post_office.EmailBackend"
POST_OFFICE = {
    "CELERY_ENABLED": True,
    "DEFAULT_PRIORITY": "now",
    "MESSAGE_ID_ENABLED": True,
    "MESSAGE_ID_FQDN": DEFAULT_DOMAIN,
    "MAX_RETRIES": 3,
    "LOG_LEVEL": 1 if not DEBUG else 2,
}

if DEBUG:
    POST_OFFICE["BACKENDS"] = {
        "default": "django.core.mail.backends.console.EmailBackend",
    }
else:
    POST_OFFICE["BACKENDS"] = {
        "default": "django.core.mail.backends.smtp.EmailBackend",
    }
    EMAIL_HOST = env.get_string("DJANGO_SMTP_HOSTNAME", "localhost")
    EMAIL_PORT = env.get_string("DJANGO_SMTP_PORT", 25)
    EMAIL_HOST_USER = env.get_string("DJANGO_SMTP_USER", "")
    EMAIL_HOST_PASSWORD = env.get_secret("DJANGO_SMTP_PASSWORD", "")
    EMAIL_USE_TLS = env.get_bool("DJANGO_SMTP_STARTTLS", False)

# Those are only used to send emails to admins and managers
SERVER_EMAIL = env.get_string("DJANGO_SERVER_EMAIL", DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = env.get_string(
    "DJANGO_EMAIL_SUBJECT_PREFIX", "[DJANGO] "
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"  # Django will search for /src/
STATICFILES_DIRS = [
    path.join(BASE_DIR, "static/"),  # Django will search for /src/
]

OIDC_OP_CONFIG_URL = (
    env.get_string("OIDC_OP_CONFIG_URL") + "/.well-known/openid-configuration"
)


DOCUMENTS_GENERATOR_DOCUMENTS_GCC_ENDPOINT = env.get_string(
    "DOCUMENTS_GENERATOR_DOCUMENTS_GCC_ENDPOINT", ""
)

STORAGES = {
    "default": {
        "BACKEND": "gccsite.storages.GCCMediaStorage"
    },

    "staticfiles": {
        "BACKEND": "gccsite.storages.GCCStaticStorage"
    }
}

AWS_ACCESS_KEY_ID = env.get_secret("DJANGO_S3_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = env.get_secret("DJANGO_S3_SECRET_KEY")

DJANGO_S3_MEDIA_BUCKET = env.get_string("DJANGO_S3_MEDIA_BUCKET")
DJANGO_S3_STATIC_BUCKET = env.get_string("DJANGO_S3_STATIC_BUCKET")
AWS_S3_ENDPOINT_URL = env.get_string("DJANGO_S3_URL")
AWS_S3_URL_PROTOCOL = "https:" if env.get_bool("DJANGO_S3_SECURE_URLS", True) else "http:"
AWS_S3_CUSTOM_DOMAIN = env.get_string("DJANGO_S3_CUSTOM_DOMAIN", None)
AWS_STATIC_LOCATION = "static"

# Phonenumber_field settings
PHONENUMBER_DB_FORMAT = "E164"
PHONENUMBER_DEFAULT_REGION = "FR"