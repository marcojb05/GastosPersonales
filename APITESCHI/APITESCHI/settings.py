"""
Django settings for APITESCHI project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
# from google.oauth2 import service_account
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')

# SECURITY WARNING: don't run with debug turned on in production!
# CAMBIAR POR FALSE O EL COMANDO EN EL DEPLOY DE RENDER (TRUE ES DEFAULT)
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

INSTALLED_APPS = [
    'api',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'APITESCHI.urls'

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

WSGI_APPLICATION = 'APITESCHI.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'finanzapp',
        'USER': 'marco',
        'PASSWORD': 'akldXLFXEulZUMxtvB7KXdRk1yVh3zNv',
        'HOST': 'oregon-postgres.render.com',
        'PORT': '5432'
    }
}


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

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Following settings only make sense on production and may break development environments.
if not DEBUG:
    # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGIN_URL = '/login/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'antonio2552001@gmail.com'
EMAIL_HOST_PASSWORD = 'tcsj qova zdml elzr'

# CIERRE DE SESIÓN POR INACTIVIDAD
# Configura el motor de almacenamiento de sesión
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# Configura el tiempo de expiración de la sesión en segundos (Ahorita 15 minutos)
SESSION_COOKIE_AGE = 1500
# Cada que el usuario hace una solicitud al servidor el tiempo de la sesion se reinicia
SESSION_SAVE_EVERY_REQUEST = True

# API OPEN EXCHANGE RATE
OPEN_EXCHANGE_RATES_API_KEY = '051f01d6b07d4ea5997f2a21d8c4c14f'

# CONEXIÓN CON GOOGLE CALENDAR
# GOOGLE_CALENDAR_CREDENTIALS = os.path.join(settings.BASE_DIR, './APITESCHI/credentials.json')
# GOOGLE_CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar']
# GOOGLE_CALENDAR_SERVICE = service_account.Credentials.from_service_account_file(
#     GOOGLE_CALENDAR_CREDENTIALS, scopes=GOOGLE_CALENDAR_SCOPES
# )
# AUTHENTICATION_BACKENDS = (
#     'social.backends.google.GoogleOAuth2',
#     # Otros backends si los tienes
#     'django.contrib.auth.backends.ModelBackend',
# )

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1066329997641-sos8ehrmq7jhjue45kc5bgic0thufu16.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '84e70ab4eb8af15fb739ba3f5b20c4d25226ee26'
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# CREDENTIALS_FILE = os.path.join(BASE_DIR, 'finanzapp-402806-84e70ab4eb8a.json')

# # Cargar las credenciales desde el archivo JSON
# credentials = service_account.Credentials.from_service_account_file(
#     CREDENTIALS_FILE,
#     scopes=['https://www.googleapis.com/auth/calendar.events']
# )
# GOOGLEDRIVE_CREDENTIALS_FILE = os.path.join(BASE_DIR, 'finanzapp-402806-84e70ab4eb8a.json')

# GOOGLE_DRIVE_CREDENTIALS = os.path.join(BASE_DIR, 'finanzapp-402806-84e70ab4eb8a.json')

# AUTHENTICATION_BACKENDS = (
#     'social_core.backends.google.GoogleOAuth2',
#     'django.contrib.auth.backends.ModelBackend',
# )

# LOGIN_URL = 'login'
# LOGOUT_URL = 'logout'
# LOGIN_REDIRECT_URL = 'home'