"""
Django settings for easyprbot_market project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from braintree import Configuration, Environment
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bjr9l^65j$j2*xs&bu3agf!6+ak9j5cfk%536qp*)czojfns)0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'market.apps.MarketConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'payment.apps.PaymentConfig',
    'admin_reorder',
    'bootstrap4',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

ROOT_URLCONF = 'easyprbot_market.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'market.context_processors.market',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'easyprbot_market.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
    'global': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'easyprbot_market',
        'USER': 'easyprbot_admin',
        'PASSWORD': '12345678',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = [
    STATIC_DIR,
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


# Настройки приложения admin_reorder
# Изменение порядка вывода моделей в админ. панеле
ADMIN_REORDER = (
    {'app': 'market', 'models': ('market.Mask', 'market.Filter')},
    {'app': 'orders', 'models': ('orders.Order', 'orders.SalesStatistic')},
    {'app': 'auth', 'models': ('auth.User', 'auth.Group')},
)

# Количество записей на одной страницев в админ. панеле
ADMIN_LIST_PER_PAGE = 20

# ID корзины товаров, используемый для извлечение ее из сессий
CART_SESSION_ID = 'cart'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Настройки платежной системы Braintree.
BRAINTREE_MERCHANT_ID = 'qsc7ntkzzdxcpx6q'
BRAINTREE_PUBLIC_KEY = 'mfx6ktp3zy4bpvbc'
BRAINTREE_PRIVATE_KEY = '10601c57d88c730abec38efb7eb87b41'

Configuration.configure(
    Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)
