
"""
Django settings for running tests
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'secret'

INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django_timer',
    'tests',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ROOT_URLCONF = 'tests.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    }
]

DEBUG = True