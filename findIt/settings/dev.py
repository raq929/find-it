from .base import *

DEBUG = True

SECRET_KEY = '!t(c@x5&d(u_3m$rd6rn-w$28llx&@v!=e&##-=utou52(bc09'

ALLOWED_HOSTS = []


INSTALLED_APPS += {
  'debug_toolbar',
}

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# debug toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ['127.0.0.1']

# Caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

CACHE_MIDDLEWARE_ALIAS = 'default'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'findit',
        'USER': 'racheltstevens',
        'PASSWORD': '$PASSWORD',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
