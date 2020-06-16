# coding: utf-8

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = os.environ.get("DEBUG", "false") in ("true", "True", "1")

SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data.db'),
    }
}

TIME_ZONE = os.environ.get('TSURU_DASHBOARD_TIME_ZONE', 'America/Sao_Paulo')

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                "django.template.context_processors.static",
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
            ],
        },
    },
]

SETTINGS_EXPORT = [
    'ELASTICSEARCH_METRICS_ENABLED',
]

ELASTICSEARCH_METRICS_ENABLED = os.environ.get("ELASTICSEARCH_METRICS_ENABLED", "true") in ['true', 'True', '1']

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'abyss.urls'

WSGI_APPLICATION = 'abyss.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tsuru_dashboard',
]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'dashboard': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'tsuru_dashboard': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    }
}

ALLOWED_HOSTS = ["*"]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'tsuru_cache',
    }
}

RVN_CONFIG = os.environ.get("RAVEN_CONFIG")
if RVN_CONFIG:
    RAVEN_CONFIG = {
        'dsn': RVN_CONFIG,
    }

    INSTALLED_APPS = INSTALLED_APPS + [
        'raven.contrib.django.raven_compat',
    ]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
