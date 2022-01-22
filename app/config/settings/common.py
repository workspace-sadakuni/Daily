import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'daily',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'daily.middleware.auth.SessionCheck'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': env.get_value('DATABASE_ENGINE', default='django.db.backends.sqlite3'),
#         'NAME': env.get_value('DATABASE_DB', default=os.path.join(BASE_DIR, 'db.sqlite3')),
#         'USER': env.get_value('DATABASE_USER', default='django_user'),
#         'PASSWORD': env.get_value('DATABASE_PASSWORD', default='password'),
#         'HOST': env.get_value('DATABASE_HOST', default='localhost'),
#         'PORT': env.get_value('DATABASE_PORT', default='5432'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# アップロード可能上限　1MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000000

# ログイン・認証用モデルの設定
AUTH_USER_MODEL = 'daily.Users'

# セッションタイム
SESSION_TIMER = 3600

# ログ保存先ディレクトリ
LOG_DIR = '/var/log/daily'
APP_LOG_DIR = LOG_DIR + '/logger'

# 500エラークラッシュログ保存先ディレクトリ
CLASH_DUMP_LOG_DIR = LOG_DIR + '/web-clash-log'

# ログ出力先ディレクトリが存在しない場合、作成
if not os.path.isdir(APP_LOG_DIR):
    os.makedirs(APP_LOG_DIR)
if not os.path.isdir(CLASH_DUMP_LOG_DIR):
    os.makedirs(CLASH_DUMP_LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s][pid:%(process)d][%(levelname)s][%(filename)s:%(lineno)d] %(message)s'
        },
        'simple': {
            'format': '[%(server_time)s]%(levelname)s %(message)s a',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'to_logfile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': APP_LOG_DIR + '/logger.log',
        }
    },
    'loggers': {
        'dev_application': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'application': {
            'handlers': ['to_logfile'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
