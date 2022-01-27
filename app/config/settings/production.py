import os
import environ

from config.settings.common import *

env = environ.Env()
env.read_env('.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get_value('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = env.get_value('ALLOWED_HOSTS')

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env.get_value('DATABASE_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': env.get_value('DATABASE_DB', default=os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': env.get_value('DATABASE_USER', default='django_user'),
        'PASSWORD': env.get_value('DATABASE_PASSWORD', default='password'),
        'HOST': env.get_value('DATABASE_HOST', default='localhost'),
        'PORT': env.get_value('DATABASE_PORT', default='5432'),
    }
}
