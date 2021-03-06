import os
# Django settings for invoicy project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = '/Users/prabhu/hacks/invoicy/db.sqllite'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'Europe/London'

LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), 'media'))

MEDIA_URL = ''

ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "invoicy.common.utils.context_processors.workflow_processor",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'invoicy.common.utils.middleware.ThreadLocalsMiddleware',
)

ROOT_URLCONF = 'invoicy.urls'

TEMPLATE_DIRS = (
    os.path.normpath(os.path.join(os.path.dirname(__file__), 'templates')),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'invoicy.guidy',
    'invoicy.clienty',
    'invoicy.exporty',
    'invoicy.common',
)

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/guidy/'

# Prefix to use for all urls. Change this parameter if you would like use
# invoicy under a different directory. For eg,
# if you want to place invoicy inside myapps dir in your webserver - http://server.com/myapps
# then set this variable as "myapps/"
# NOTE: Set FORCE_SCRIPT_NAME with the same value if things dont work.
URL_PREFIX = ''

FORCE_SCRIPT_NAME = ''

# Caching configs.
CACHE_BACKEND = 'locmem:///'

# Import any private settings.
try:
    from localsettings import *
except:
    pass
