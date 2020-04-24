from .base_settings import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

MIDDLEWARE = [
                 'debug_toolbar.middleware.DebugToolbarMiddleware',
                 # middleware for debug toolbar, should be set at top
             ] + MIDDLEWARE

INSTALLED_APPS += [
    'django.contrib.staticfiles',  # serving static files for development
    'debug_toolbar',  # debug toolbar for development
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

############################################################################

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# Django perform a not effective way to collect all static files in each app and combine them together
# static files
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files besides static folder in each app (if exists)
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]

# media files: media, GIFs, videos, etc.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

############################################################################

# DEBUG toolbar settings

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECT': False,
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}
