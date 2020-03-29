from .base_settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'slinkydb_notgrubhub',
        'USER': 'cinnamon',
        'PASSWORD': os.environ.get('DB_PASSWORD', ""),
        'HOST': 'slinkydb.cof5tctkml6g.us-west-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# TODO: EMAIL VERIFICATION, S3 BUCKET STATIC FILES, Serving static files for production