"""
Django settings for SIRENE project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key
from django.contrib.messages import constants as messages


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# ./django <=> [docker] = /app  with manage.py
#print(f"BASE_DIR = {BASE_DIR}")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", default=get_random_secret_key())
#DEBUG = True
DEBUG = int(os.environ.get("DJANGO_DEBUG", default=1))
try:
   ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
except:
   ALLOWED_HOSTS = ['*']

try:
    #CSRF_TRUSTED_ORIGINS=['http://localhost:8000','http://192.168.0.11:8000','http://localhost:4180'] 
    CSRF_TRUSTED_ORIGINS = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS").split(" ")
except:
    CSRF_TRUSTED_ORIGINS = ['http://localhost:8000','http://192.168.0.11:8000','http://localhost:4180']


# -------------------------------------------------------------------
# Application definition
# -------------------------------------------------------------------
SIRENE_APPS = [
    'app_sirene.apps.AppSireneConfig',
    'app_home.apps.AppHomeConfig',
    'app_user.apps.AppUserConfig',
    'app_conf.apps.AppConfConfig',
    'app_log.apps.AppLogConfig',
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
        'DIRS': [BASE_DIR / 'templates2', BASE_DIR / 'templates/'],
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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DJANGO_SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DJANGO_SQL_DATABASE", BASE_DIR / "../db.sqlite3"),
        "USER": os.environ.get("DJANGO_SQL_USER", "user"),
        "PASSWORD": os.environ.get("DJANGO_SQL_PASSWORD", "password"),
        "HOST": os.environ.get("DJANGO_SQL_HOST", "localhost"),
        "PORT": os.environ.get("DJANGO_SQL_PORT", "3306"),
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
# Cache
# -------------------------------


CACHES = {
    # … default cache config and others
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://sirene_redis:6379/0",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient" }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://sirene_redis:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient" }
    },
    # "select2": {
    #     "BACKEND": "django_redis.cache.RedisCache",
    #     "LOCATION": "redis://sirene_redis:6379/2",
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
SESSION_COOKIE_AGE = 3600
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'


# -------------------------------
# Celery
# -------------------------------

CELERY_BROKER_URL = os.environ.get("DJANGO_CELERY_BROKER_URL", default="redis://sirene_redis:6379")
CELERY_RESULT_BACKEND = os.environ.get("DJANGO_CELERY_RESULT_BACKEND", default="redis://sirene_redis:6379")
    

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
# unittest TEST_MODE
# -------------------
#SIRENE_TEST_USER = None

# -------------------
# DEBUG Toolbar
# -------------------

# Docker
if DEBUG:
    import socket  # only if you haven't already imported this
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    #print(hostname, ips)
    #INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

# manually : nginx RP IP
if DEBUG:
    INTERNAL_IPS = [
        # ...
        "127.0.0.1",
        # "192.168.0.11",
        "172.18.0.1",
        "172.18.0.2",
        "172.18.0.3",
        "172.18.0.4",
        "172.18.0.5",
        "172.18.0.6",
    ]

# # Docker
# if DEBUG:
#     import socket  # only if you haven't already imported this
#     hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#     INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

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
EMAIL_HOST         = os.environ.get("SIRENE_EMAIL_HOST", default="localhost")
EMAIL_PORT         = int(os.environ.get("SIRENE_EMAIL_PORT", default=25))
EMAIL_HOST_USER = os.environ.get("SIRENE_EMAIL_USER","")
EMAIL_HOST_PASSWORD = os.environ.get("SIRENE_EMAIL_PASSWORD","")

if EMAIL_PORT == 465:
    EMAIL_USE_SSL = True   

if EMAIL_PORT == 587:
    EMAIL_USE_TLS = True   

# -------------------------------
# SMS Provider
# -------------------------------

# stdout, folder, clicsecure
SIRENE_SMS_URL       = os.environ.get("SIRENE_SMS_URL","https://localhost/")
SIRENE_SMS_LOGIN     = os.environ.get("SIRENE_SMS_LOGIN","sirene")
SIRENE_SMS_PASSWORD  = os.environ.get("SIRENE_SMS_PASSWORD","changeme")

