"""Development settings and globals."""

from __future__ import absolute_import
from os.path import join, normpath
from .base import *
import debug_toolbar

DEBUG = True
ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'solar_energy',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '',
    }
}

PGPASSWORD=root pg_dump -Fc --no-acl --no-owner -h localhost -U root solar_energy > mydb.dump
heroku pg:push mydb.dump HEROKU_POSTGRESQL_MAGENTA --app sushi

INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
