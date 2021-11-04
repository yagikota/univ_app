from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '-p#udqdkhhb%x^6fu1t7@=2^*-smixzpi52*dmu+9fql6h&5+i'
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True
DEBUG = os.environ.get("DEBUG")

# ALLOWED_HOSTS = ["fudai-kenja.com"]
# ALLOWED_HOSTS = ["*"]
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.mainConfig',
    'bootstrap4',
    'widget_tweaks',
    'pure_pagination',
    # django-allauthを使用するのに必要
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

# django-allauthを使用するのに必要
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

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
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'fudai_kenja_db',
#         'USER': 'kotayagi',
#         'PASSWORD': 'aullfetalflchemist',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.environ.get("SQL_DATABASE"),
#         'USER': os.environ.get("SQL_USER"),
#         'PASSWORD': os.environ.get("SQL_PASSWORD"),
#         'HOST': os.environ.get("SQL_HOST"),
#         'PORT': os.environ.get("SQL_PORT"),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# メール送信の処理
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = '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'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# 暗号化されたhttpsを使うようにする
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True

# django-allauthの設定
LOGIN_REDIRECT_URL = '/top_page/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True 
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'# the user is blocked from logging in until the email address is verified
ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_SUBJECT_PREFIX = '[fudai-kenja.com] '
ACCOUNT_MAX_EMAIL_ADDRESSES = 2
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_ADAPTER = 'main.adapter.ExtendedAccountAdapter'


PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 2,
    'MARGIN_PAGES_DISPLAYED': 1,
    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}

AUTH_USER_MODEL = 'main.User'
