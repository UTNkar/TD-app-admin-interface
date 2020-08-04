from adminInterface.settings.base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

ALLOWED_HOSTS = [".utn.se"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET',
    'deg=*gpfq%ymtn-!ws#_g^-4r94cn=3n^=w!yig+6u%=hz#5b0'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DJANGO_DB_NAME', 'admininterface'),
        'USER': os.environ.get('DJANGO_DB_USER', 'admininterface'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASS'),
        'HOST': os.environ.get('DJANGO_DB_HOST', '127.0.0.1'),
        'PORT':  os.environ.get('DJANGO_DB_PORT', '5432'),
    }
}

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_DOMAIN = '.utn.se'

SESSION_COOKIE_SECURE = True

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

KRONOS_PREFIX = (
    'export GOOGLE_APPLICATION_CREDENTIALS="admininterface-privatekey.json" && '
    'export SENTRY_DSN="{0}" &&'.format(os.environ.get("SENTRY_DSN"))
)
