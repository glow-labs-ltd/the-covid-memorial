# flake8: noqa
from .base import *

db_user = os.environ.get('POSTGRES_USERNAME')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DATABASE_NAME')
db_connection_name = os.environ.get('POSTGRES_CONNECTION_NAME')

DEBUG = False

SECURE_SSL_REDIRECT = True

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': '/cloudsql/{}'.format(db_connection_name),
        'PORT': '5432',
        'CONN_MAX_AGE': 300,
    }
}
