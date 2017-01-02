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

DATABASES = {}
DATABASES['default'] =  dj_database_url.config()

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'


def get_cache():
  try:
    os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
    os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
    os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

    return {
      'default': {
          # Use pylibmc
          'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',

          # Use binary memcache protocol (needed for authentication)
          'BINARY': True,

          'TIMEOUT': 500, # 5 minutes

          'OPTIONS': {
              # Enable faster IO
              'tcp_nodelay': True,

              # Keep connection alive
              'tcp_keepalive': True,

              # Timeout settings
              'connect_timeout': 2000, # ms
              'send_timeout': 750 * 1000, # us
              'receive_timeout': 750 * 1000, # us
              '_poll_timeout': 2000, # ms

              # Better failover
              'ketama': True,
              'remove_failed': 1,
              'retry_timeout': 2,
              'dead_timeout': 30,
          }
      }
  }
  except:
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
      }
    }

CACHES = get_cache()
