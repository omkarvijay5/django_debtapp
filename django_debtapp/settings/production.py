from .base import *

DEBUG = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'debtdb',                 # Or path to database file if using sqlite3.
#         'USER': 'vijay',                 # Not used with sqlite3.
#         'PASSWORD': 'vijay',         # Not used with sqlite3.
#         'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#     }
# }


DEFAULT_FROM_EMAIL = 'omkarvijay5@gmail.com'
SERVER_EMAIL = 'omkarvijay5@gmail.com'

ALLOWED_HOSTS = ['django-debtapp.herokuapp.com']

import dj_database_url
DATABASES['default'] =  dj_database_url.config()