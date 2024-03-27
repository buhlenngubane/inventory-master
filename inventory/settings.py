"""
Django settings for inventory project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import dj_database_url
import django_heroku
import os
from dotenv import load_dotenv
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR+ "/"+ "sent_emails"
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv('DEBUG') == "1" else False

# LOGIN_URL = 'login'
print(DEBUG)
print(os.getenv('DEBUG'))

ALLOWED_HOSTS = [
    # '*'
    '127.0.0.1'
]
SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',

    'item',
    'store',
    # 'django_google_fonts',
    'widget_tweaks',

    #'stock_control.apps.StockControlConfig',
    #'accounts.apps.AccountsConfig',
    # 'email_service.apps.EmailServiceConfig',
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'
AUTH_USER_MODEL = 'accounts.Employee'
# GOOGLE_FONTS = ["Kablammo", "Roboto:300"]

MIDDLEWARE = [
    # 'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventory.urls'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
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

# LOGIN_URL = 'login'

WSGI_APPLICATION = 'inventory.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# TESTING_MODE = DEBUG
if not DEBUG:
    DATABASES = {
        'default': 
            dj_database_url.parse(os.getenv('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': 
            dj_database_url.parse(os.getenv('DATABASE_URL'))
    }
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': 'db.sqlite3',
    #     }
    # }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

LOGIN_REDIRECT_URL = 'item:index'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL

# Configure Django App for Heroku.
django_heroku.settings(locals())
TEST_RUNNER = 'django_heroku.HerokuDiscoverRunner'
# # # Email services
# EMAIL_BACKEND = "anymail.backends.sparkpost.EmailBackend"
# DEFAULT_FROM_EMAIL = ''
# ANYMAIL = {
#     'IGNORE_UNSUPPORTED_FEATURES': True,
#     'SPARKPOST_API_KEY': '',
#     'SPARKPOST_API_URL': '',
# }
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_POST = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''#os.environ.get('traces_email_password')
