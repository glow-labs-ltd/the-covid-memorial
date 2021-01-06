# flake8: noqa
import os

from .base import *

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

ALLOWED_HOSTS = [
    '*',
]

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
