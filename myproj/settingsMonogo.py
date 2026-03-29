import os
from pathlib import Path
from decouple import config, Csv

# 1. BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. SECURITY
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='.vercel.app,localhost,127.0.0.1', cast=Csv())

# 3. APPLICATION DEFINITION
INSTALLED_APPS = [
    'cloudinary_storage', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    'cloudinary',
    'django.contrib.humanize',
    'django.contrib.sites',
    'whitenoise.runserver_nostatic',
    'widget_tweaks',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    'django_filters',
    'import_export',
    'rest_framework',
    'investments_appraisal.apps.InvestmentsAppraisalConfig',    
    'businessforum.apps.BusinessforumConfig',
    'trading.apps.TradingConfig',
    'fishapp.apps.FishappConfig',
    'beefapp.apps.BeefappConfig',
    'common.apps.CommonConfig',
    'comment', 
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middlewares.OneSessionPerUserMiddleware',
]

ROOT_URLCONF = 'myproj.urls'

# 4. MONGODB DATABASE (using Djongo)
DATABASE_URL = config('DATABASE_URL')

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'clearvision', 
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': DATABASE_URL,
            'retryWrites': True,
            'w': 'majority',
        }
    }
}

# Note: PostgreSQL 'sslmode' removed as MongoDB uses SRV + SSL natively in the connection string.

# 5. STATIC & MEDIA FILES
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "myproj" / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles_build" / "static"

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default='dsbnt7cih'),
    'API_KEY': config('CLOUDINARY_API_KEY', default='729236266824714'),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default='JZXOjGXheadh0YtH7Ip7Nbu_yv0'),
    'STATICFILES_STORAGE': None, 
}

# 6. PRODUCTION SETTINGS
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

    # Non-manifest storage to prevent Vercel 500 errors
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    WHITENOISE_MANIFEST_STRICT = False
    WHITENOISE_KEEP_ONLY_HASHED_FILES = True
else:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# 7. TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'myproj' / 'templates'],
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

WSGI_APPLICATION = 'myproj.wsgi.application'

# 8. INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Harare' 
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'