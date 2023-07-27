"""
Django settings for big_data_sample_prj project.

Generated by 'django-admin startproject' using Django 3.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

# package
import os
from dotenv import load_dotenv
import datetime
from pathlib import Path

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-++u$m=&)u7(@e)+7tc5%1qknhf$4zrr9kf%x@z9@1v*wfwtoq!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Rest framework 設定
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

# swagger 設定
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        "basic": {
            'type': 'basic'
        }
    },
    'DEFAULT_INFO': 'server.urls.openapi_info',
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    "enabled_methods": [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    'APIS_SORTER': 'alpha',
    'JSON_EDITOR': True,
    'OPERATIONS_SORTER': 'alpha',
    'VALIDATOR_URL': None,
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ['Bearer'],
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(minutes=30)
}

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'drf_yasg',
    'base_app',
    'article',
    'paragraph',
    'comment',
    'emoji',
    'media',
    'tag'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'big_data_sample_prj.urls'
CORS_URLS_REGEX = r"^/.*"
CORS_ALLOW_HEADERS = [
    "Accept",
    "content-type",
    "Authorization"
]
CORS_EXPOSE_HEADERS = [
    "Accept",
    "content-type",
    "Authorization"
]

ALLOWED_HOSTS = [os.getenv("WITHOUT_HTTPS_DOMAINS")]
CORS_ALLOWED_ORIGINS = [os.getenv("DOMAINS")]
CSRF_TRUSTED_ORIGINS = [os.getenv("DOMAINS")]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'big_data_sample_prj.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USERNAME"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',  # 數據插入被截斷，會將警告升級為錯誤
            'charset': 'utf8mb4',
            'init_command': "SET collation_connection = 'utf8mb4_unicode_ci'",
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = ''
MEDIA_ROOT = os.path.join(BASE_DIR, '')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
