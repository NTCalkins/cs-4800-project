from .base_settings import *
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# media files: media, GIFs, videos, etc.
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

# TODO: EMAIL VERIFICATION, S3 BUCKET STATIC FILES, Serving static files for production

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')

AWS_S3_FILE_OVERWRITE = config('AWS_S3_FILE_OVERWRITE')
AWS_DEFAULT_ACL = config('AWS_DEFAULT_ACL')
DEFAULT_FILE_STORAGE = config('DEFAULT_FILE_STORAGE')
STATICFILES_STORAGE = config('DEFAULT_FILE_STORAGE')
