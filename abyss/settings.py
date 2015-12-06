# coding: utf-8

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = os.environ.get("DEBUG", "false") in ("true", "True", "1")

TEMPLATE_DEBUG = DEBUG

SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data.db'),
    }
}

TIME_ZONE = 'America/Sao_Paulo'

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static_files'),
    'tsuru_dashboard/dashboard/static_files',
    'tsuru_dashboard/apps/static_files',
    'tsuru_dashboard/admin/static_files',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "tsuru_dashboard.autoscale.context_processors.autoscale_enabled",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'abyss.urls'

WSGI_APPLICATION = 'abyss.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tsuru_dashboard.auth',
    'tsuru_dashboard.apps',
    'tsuru_dashboard.services',
    'tsuru_dashboard.teams',
    'tsuru_dashboard.healthcheck',
    'tsuru_dashboard.admin',
    'tsuru_dashboard.autoscale',
    'tsuru_dashboard.dashboard',
    'tsuru_dashboard.metrics',
)

TSURU_HOST = os.environ.get("TSURU_HOST", "http://localhost:8080")

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
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
            'level': 'INFO',
            'propagate': True,
        },
        'dashboard': {
            'handlers': ['console'],
            'level': 'INFO',
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

    INSTALLED_APPS = INSTALLED_APPS + (
        'raven.contrib.django.raven_compat',
    )
