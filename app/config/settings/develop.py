import os
import environ

from config.settings.common import *

SECRET_KEY = '*uma=anyry6!5zcx@^2k7lr&ejr6bsd&74t@w6lqo%lsfa9=rc'

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Daily',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}

# ローカル環境用設定ファイルをimport。正しく上書くため、develop.pyの最後に記述。
try:
    # gitにcommitしない一時的な設定はlocal.pyに記載
    from config.settings.local import *
except ImportError as e:
    pass
