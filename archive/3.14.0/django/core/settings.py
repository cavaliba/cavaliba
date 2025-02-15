"""
Django settings for CAVALIBA
"""

import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key
from django.contrib.messages import constants as messages


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# ./django <=> [docker] = /app  with manage.py



SECRET_KEY = os.environ.get("CAVALIBA_SECRET_KEY", default=get_random_secret_key())
#DEBUG = True
DEBUG = int(os.environ.get("CAVALIBA_DEBUG", default=1))
try:
   ALLOWED_HOSTS = os.environ.get("CAVALIBA_ALLOWED_HOSTS").split(" ")
except:
   ALLOWED_HOSTS = ['*']

try:
    CSRF_TRUSTED_ORIGINS = os.environ.get("CAVALIBA_CSRF_TRUSTED_ORIGINS").split(" ")
except:
    CSRF_TRUSTED_ORIGINS = ['http://localhost:8000','http://192.168.0.11:8000','http://localhost:4180']


# -------------------------------------------------------------------
# Application definition
# -------------------------------------------------------------------
SIRENE_APPS = [
    'app_sirene.apps.AppSireneConfig',
    'app_home.apps.AppHomeConfig',
    'app_user.apps.AppUserConfig',
    'app_data.apps.AppDataConfig',
]

INSTALLED_APPS =  SIRENE_APPS + [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'debug_toolbar',
    ]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'core.urls'

# -------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [ BASE_DIR / 'templates_custom', BASE_DIR / 'templates/'],
        'DIRS': [ "/files/templates/", BASE_DIR / 'templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app_home.context_processor.get_info', # <-- Add your context processor
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# -------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
# -------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = "/static_collect"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# -------------------------------------------------------------------
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# -------------------------------------------------------------------


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("CAVALIBA_DB_ENGINE", "django.db.backends.sqlite3"),
        "HOST": os.environ.get("CAVALIBA_DB_HOST", "localhost"),
        "PORT": os.environ.get("CAVALIBA_DB_PORT", "3306"),
        "NAME": os.environ.get("CAVALIBA_DB_DATABASE", BASE_DIR / "../db.sqlite3"),
        "USER": os.environ.get("CAVALIBA_DB_USER", "user"),
        "PASSWORD": os.environ.get("CAVALIBA_DB_PASSWORD", "password"),
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# -------------------------------
# Django Login Workflow
# -------------------------------

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/home/private'

# -------------------------------
# Cache
# -------------------------------


CACHES = {
    # … default cache config and others
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://cavaliba_redis:6379/0",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient" }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://cavaliba_redis:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient" }
    },
    # "select2": {
    #     "BACKEND": "django_redis.cache.RedisCache",
    #     "LOCATION": "redis://cavaliba_redis:6379/2",
    #     "OPTIONS": { "CLIENT_CLASS": "django_redis.client.DefaultClient" }
    # }
}

# Tell select2 which cache configuration to use:
#SELECT2_CACHE_BACKEND = "select2"

# -------------------------------
# Sessions
# -------------------------------

#SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_CACHE_ALIAS = 'session'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = int(os.environ.get("CAVALIBA_SESSION_DURATION", default=3600))

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'


# -------------------------------
# Celery
# -------------------------------

CELERY_BROKER_URL = os.environ.get("CAVALIBA_CELERY_BROKER_URL", default="redis://cavaliba_redis:6379")
CELERY_RESULT_BACKEND = os.environ.get("CAVALIBA_CELERY_RESULT_BACKEND", default="redis://cavaliba_redis:6379")
    

# -------------------------------
# Common
# -------------------------------


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
USE_I18N = True
LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'
USE_TZ = True
TIME_ZONE = 'Europe/Paris'



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Flash message
#from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# # translation files
# LOCALE_PATHS = [
#     BASE_DIR / "locale",
# ]

FIXTURE_DIRS = [
    BASE_DIR / "fixture",
]


# -------------------
# DEBUG Toolbar
# -------------------

# Docker
if DEBUG:
    INTERNAL_IPS =  os.environ.get("CAVALIBA_DEBUG_IP","127.0.0.1").split(" ")

# -------------------
# TinyMCE
# -------------------
# TINYMCE_JS_URL (default: settings.STATIC_URL + 'tinymce/tinymce.min.js')
# The URL of the TinyMCE javascript file:
# TINYMCE_JS_URL = os.path.join(STATIC_URL, "path/to/tiny_mce/tiny_mce.js")


TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 500,
    "menubar": False,
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
    "code,help,wordcount",
    "toolbar": "undo redo | formatselect | link |"
    "bold italic backcolor | alignleft aligncenter "
    "alignright alignjustify | bullist numlist outdent indent | "
    "removeformat | code | preview | help",
    "relative_urls": 0,
    "remove_script_host": 0,
}

TINYMCE_COMPRESSOR = False
TINYMCE_SPELLCHECKER = False 
TINYMCE_FILEBROWSER = False 

# -------------------------------------------------------------------
# APP SIRENE
# -------------------------------------------------------------------

# -------------------
# EMAIL GENERAL SETUP
# -------------------
EMAIL_HOST         = os.environ.get("CAVALIBA_EMAIL_HOST", default="localhost")
EMAIL_PORT         = int(os.environ.get("CAVALIBA_EMAIL_PORT", default=25))
EMAIL_HOST_USER = os.environ.get("CAVALIBA_EMAIL_USER","")
EMAIL_HOST_PASSWORD = os.environ.get("CAVALIBA_EMAIL_PASSWORD","")

if EMAIL_PORT == 465:
    EMAIL_USE_SSL = True   

if EMAIL_PORT == 587:
    EMAIL_USE_TLS = True   
