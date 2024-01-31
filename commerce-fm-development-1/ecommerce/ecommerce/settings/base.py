import os
import yaml
from django.core.exceptions import ImproperlyConfigured
from datetime import timedelta

credentials = yaml.load(open('config/config.yaml'), Loader=yaml.FullLoader)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = credentials['SECRET_KEY']
DEBUG = credentials['DEBUG']
ALLOWED_HOSTS = credentials['ALLOWED_HOSTS']

GEOIP_PATH = BASE_DIR+"/GeoData/GeoLite2-City.mmdb"

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

THIRD_PARTY_APPS = [
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'security',
    'rest_framework_simplejwt.token_blacklist',
    'user_agents'
]
OWN_APPS = [
    'Api',
    'User',
    'Vendor',
    'Products',
    'frontend',
    'Analytics',
    'CartSystem',
    'DashboardManagement',
    'OrderAndDelivery',
    'Offer',
    'CompanyInformation',
    'Referral',
    'DeliverySystem'
]

INSTALLED_APPS += THIRD_PARTY_APPS + OWN_APPS
AUTH_USER_MODEL = 'User.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # django-security
    'security.middleware.DoNotTrackMiddleware',
    'security.middleware.ContentNoSniff',
    'security.middleware.XssProtectMiddleware',
    'security.middleware.XFrameOptionsMiddleware',

    # Own
    'ecommerce.middlewares.ip.IpAddress'
]

ROOT_URLCONF = 'ecommerce.urls'

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
                'DashboardManagement.context_processor.context_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# Database
if DEBUG:
    from .development import *
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
else:
    from .production import *

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGIN_URL = '/dashboard/login'

STATIC_URL = '/static/'
MEDIA_URL = '/media'
STATICFILES_DIRS = [BASE_DIR+"/assets", ]
STATIC_ROOT = BASE_DIR+'/static'
MEDIA_ROOT = BASE_DIR+'/media'
MEDIA_URL = '/media/'

try:
    # System
    MULTI_VENDOR = credentials['MULTI_VENDOR']
    ADD_TO_CART_WITHOUT_LOGIN = credentials['ADD_TO_CART_WITHOUT_LOGIN']
    HAS_ADDITIONAL_USER_DATA = credentials['HAS_ADDITIONAL_USER_DATA']
    MUST_HAVE_ADDITIONAL_DATA = credentials['MUST_HAVE_ADDITIONAL_DATA']
    TEMPLATE_VERSION = credentials['TEMPLATE_VERSION']
    COMPANY_NAME = credentials['COMPANY_NAME']
    HAS_OFFER_APP = credentials['HAS_OFFER_APP']
    DISPLAY_OUT_OF_STOCK_PRODUCTS = credentials['DISPLAY_OUT_OF_STOCK_PRODUCTS']
    JWT_SECRET = credentials['jwt_secret']
    HAS_REFERRAL_APP = credentials['HAS_REFERRAL_APP']
    HAS_VENDOR_REFERRAL_APP = credentials['HAS_VENDOR_REFERRAL_APP']
    FRONTEND_URL = credentials['FRONTEND_URL']
    FRONTEND_REFER_URL = credentials['FRONTEND_REFER_URL']

    # Email
    EMAIL_USE_TLS = credentials['EMAIL_USE_TLS']
    EMAIL_HOST = credentials['smtp_server']
    EMAIL_HOST_USER = credentials['sys_email']
    EMAIL_HOST_PASSWORD = credentials['sys_password']
    EMAIL_PORT = credentials['smtp_port']
    EMAIL_USE_SSL = credentials['EMAIL_USE_SSL']
    HAS_CELERY = credentials['HAS_CELERY']
    CELERY_FOR_EMAIL = credentials['CELERY_FOR_EMAIL']

    if HAS_CELERY:
        CELERY_BROKER_URL = credentials['CELERY_BROKER_URL']
        CELERY_ACCEPT_CONTENT = ['json']
        CELERY_TASK_SERIALIZER = 'json'
except (Exception, KeyError) as e:
    raise ImproperlyConfigured("Config.yaml is not properly set.", e)

TIME_INPUT_FORMATS = ['%I:%M %p', ]

# CKEditor
CKEDITOR_CONFIGS = {
    'default': {
        'width': 'unset',
        'height': 'unset',
    }
}

CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_UPLOAD_PATH = "uploads/"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': JWT_SECRET,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'email',
    'USER_ID_CLAIM': 'email',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}
