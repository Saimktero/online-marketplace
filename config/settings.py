import os
from decouple import config
import dj_database_url
from datetime import timedelta
from pathlib import Path
from rest_framework.authentication import SessionAuthentication
from config.celery import celery_app

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: v.split(','))

INTERNAL_IPS = ['127.0.0.1']

# Приложения и middleware
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'debug_toolbar',
    'corsheaders',
    'core',
    'whitenoise.runserver_nostatic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://marketplace-frontend-production-0785.up.railway.app',
]

CSRF_TRUSTED_ORIGINS = [
    'https://online-marketplace-production-d156.up.railway.app',
    'https://marketplace-frontend-production-0785.up.railway.app',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Настройка базы данных
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}


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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
                  'PAGE_SIZE': 10,
                  'DEFAULT_FILTER_BACKENDS': [
                      'django_filters.rest_framework.DjangoFilterBackend',
                      'rest_framework.filters.SearchFilter',
                  ],
                  'DEFAULT_AUTHENTICATION_CLASSES': [
                      'rest_framework_simplejwt.authentication.JWTAuthentication',
                  ],
                  'DEFAULT_PERMISSION_CLASSES': [
                      'rest_framework.permissions.AllowAny'
                  ],

                  }

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Отключаем проверку CSRF


__all__ = ('celery_app',)

# Настройки Celery
CELERY_BROKER_URL = config("REDIS_URL")  # Брокер сообщений
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# Настройка хранения результатов задач (backend)
CELERY_RESULT_BACKEND = config("REDIS_URL")

# Настройки отправки email через SMPT (пример для Gmail)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  # SMPT-сервер Gmail
EMAIL_PORT = 587  # Порт SMTP (587 для TLS, 465 для SSL)
EMAIL_USE_TLS = True  # Включаем TLS (если используется SSL, нужно EMAIL_USE_SSL = True)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')  # Мой email
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')  # Пароль (или App Password, если включена двухфакторка)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Включение кеширования прав доступа
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

AUTH_PERMISSION_CACHE = True

"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
"""
