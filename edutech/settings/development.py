from .base import *

DEBUG=True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#media settings
MEDIA_URL='media/'
MEDIA_ROOT=BASE_DIR / "mediafiles"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = 'fb3596f0f408c7'
EMAIL_HOST_PASSWORD = '435604dbc85d2d'
EMAIL_PORT = '2525'
DEFAULT_FROM_EMAIL="support@edutech.com"
SITE_NAME="edutech"