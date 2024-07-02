from pathlib import Path
import environ
from datetime import timedelta


env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

environ.Env.read_env(BASE_DIR / ".env")


SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
SITE_ID=1

THIRD_PARTY_APPS=[
   'rest_framework',
   "corsheaders",
    'rest_framework_simplejwt.token_blacklist',
]

LOCAL_APPS=[
    'apps.users',
    'apps.profiles',
    'apps.courses'
]

INSTALLED_APPS= DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

CORS_ALLOWED_ORIGINS=[
    "http://localhost:3000"
]

CORS_ALLOW_CREDENTIALS=True
# CSRF_TRUSTED_ORIGINS = [
#     "https://read-and-write.example.com",
# ]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'edutech.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.users.authentication.CustomJwtAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
}

AUTH_USER_MODEL='users.CustomUser'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    "AUTH_COOKIE":"jwt_access",
    "AUTH_COOKIE_SECURE":True,
    "AUTH_COOKIE_HTTPONLY":True,
    "AUTH_COOKIE_DOMAIN":None,
    "AUTH_COOKIE_SAMESITE":"None",
    "AUTH_COOKIE_PATH":"/",
    "AUTH_COOKIE_REFRESH":"jwt_refresh",
    'AUTH_COOKIE_ACCESS_MAX_AGE':60 * 30,
    'AUTH_COOKIE_REFRESH_MAX_AGE':60 * 60 * 24
}

# DJOSER = {
#     'LOGIN_FIELD': 'email',
#     'USER_CREATE_PASSWORD_RETYPE': True,
#     'SEND_ACTIVATION_EMAIL': True,
#     'ACTIVATION_URL': 'auth/activate/{uid}/{token}/',
#     'SERIALIZERS': {
#         'user_create': 'apps.users.serializers.CustomUserCreateSerializer',
#         'user_activation': 'apps.users.serializers.CustomActivationSerializer',
#         'user_create_password_retype': 'djoser.serializers.UserCreatePasswordRetypeSerializer',
#     },
#     'EMAIL':{
#     'activation': 'djoser.email.ActivationEmail',
#     'confirmation': 'djoser.email.ConfirmationEmail',
#     'password_reset': 'djoser.email.PasswordResetEmail',
#     'password_changed_confirmation': 'djoser.email.PasswordChangedConfirmationEmail',
#     'username_changed_confirmation': 'djoser.email.UsernameChangedConfirmationEmail',
#     'username_reset': 'djoser.email.UsernameResetEmail',
#     }

# }

WSGI_APPLICATION = 'edutech.wsgi.application'


GOOGLE_CLIENT_ID=env('GOOGLE_CLIENT')
GOOGLE_CLIENT_SECRET=env('GOOGLE_SECRET')
SERVER_PASSWORD=env('SECRET_PASSWORD')



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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES = [BASE_DIR / "staticfiles"]
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
