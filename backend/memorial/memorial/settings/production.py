# flake8: noqa
from .base import *

ALLOWED_HOSTS = [
    '.appspot.com',
]

DEBUG = False
SECURE_SSL_REDIRECT = True
SECRET_KEY = os.environ.get('SECRET_KEY')

db_user = os.environ.get('POSTGRES_USERNAME')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DATABASE_NAME')
db_connection_name = os.environ.get('POSTGRES_CONNECTION_NAME')

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

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_EXPIRATION = timedelta(seconds=60)
GS_FILE_OVERWRITE = False
GS_PUBLIC_BUCKET_NAME = os.environ.get('GS_PUBLIC_BUCKET_NAME')
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(
        os.path.dirname(BASE_DIR),
        'gcs_service_account.json',
    )
)
