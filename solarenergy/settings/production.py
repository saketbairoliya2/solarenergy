"""Production settings and globals."""

from __future__ import absolute_import
from os import environ
from .base import *
import dj_database_url


# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

DEBUG = False
ALLOWED_HOSTS = ['.herokuapp.com']


########## DATABASE CONFIGURATION
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

STATIC_URL = '/static/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'saketbairoliya2@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
