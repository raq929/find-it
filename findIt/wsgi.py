"""
WSGI config for findIt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.cache.backends.memcached import BaseMemcachedCache
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "findIt.settings")

# Fix django closing connection to MemCachier after every request (#11331)
BaseMemcachedCache.close = lambda self, **kwargs: None

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
