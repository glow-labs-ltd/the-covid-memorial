# flake8: noqa
import os

from .base import *

ALLOWED_HOSTS = [
    '*',
]

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'memorial',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 0,
    },
}

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

LOGGING['loggers']['django']['level'] = 'INFO'
LOGGING['loggers']['']['level'] = 'DEBUG'

# Add SQL queries to log
# LOGGING['loggers']['django.db.backends'] = {
#     'level': 'DEBUG',
# }

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
    'rest_framework.renderers.BrowsableAPIRenderer'
)
REST_FRAMEWORK['DEFAULT_METADATA_CLASS'] = 'rest_framework.metadata.SimpleMetadata'
