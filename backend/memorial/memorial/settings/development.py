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
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
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
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []

GS_PUBLIC_BUCKET_NAME = 'tcm-test-989aa9b5-319a-470e-876c-d9ba2131c1c1'

try:
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        os.path.join(os.path.dirname(BASE_DIR), 'test_service_account.json')
    )
except FileNotFoundError:
    GS_CREDENTIALS = None
