import os

import dj_database_url

from .base import *

DEBUG = False
TEMPLATE_INDEX = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['*']

SECURE_PROXY_SSL_SERVER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

EMAIL_HOST = os.environ.get('POSTMARK_SMTP_SERVER')
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('POSTMARK_API_TOKEN')
EMAIL_HOST_PASSWORD = os.environ.get('POSTMARK_API_TOKEN')
EMAIL_USE_TLS = True

TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

DATABASES['default'] =  dj_database_url.config()
