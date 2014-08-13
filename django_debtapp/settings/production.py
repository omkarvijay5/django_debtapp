from base import *

DEBUG = False

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Or path to database file if using sqlite3.
        'NAME': 'debtdb',
        'USER': 'vijay',
        'PASSWORD': 'vijay',
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
    }
}


DEFAULT_FROM_EMAIL = 'omkarvijay5@gmail.com'
SERVER_EMAIL = 'omkarvijay5@gmail.com'
ALLOWED_HOSTS = ['django-debtapp.herokuapp.com']

STATIC_FILES_DIRS = ()

import dj_database_url
DATABASES['default'] = dj_database_url.config()
