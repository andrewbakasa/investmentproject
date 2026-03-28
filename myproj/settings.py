import os
import dj_database_url
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
    'cloudinary_storage', # Must be ABOVE staticfiles
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    
    'django.contrib.humanize',
    'django.contrib.sites',

    # Third Party
    'whitenoise.runserver_nostatic',
    'widget_tweaks',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    'django_filters',
    'import_export',
    'rest_framework',

    # Your Apps
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

# 4. DATABASE
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

if not DEBUG:
    DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}

# 5. STATIC & MEDIA FILES
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'myproj', 'static'),
]

# Media handled by Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default='dsbnt7cih'),
    'API_KEY': config('CLOUDINARY_API_KEY', default='729236266824714'),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default='JZXOjGXheadh0YtH7Ip7Nbu_yv0'),
}

# 6. PRODUCTION SETTINGS (Security & Static Storage)
if not DEBUG:
    # Security Headers
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

    # WhiteNoise Optimizations
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    WHITENOISE_MANIFEST_STRICT = False  # Prevents 500 errors if an icon/file is missing
    WHITENOISE_KEEP_ONLY_HASHED_FILES = True

# 7. TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'myproj', 'templates')],
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
# import os
# import dj_database_url
# from pathlib import Path
# from decouple import config, Csv

# # 1. BASE DIRECTORY
# BASE_DIR = Path(__file__).resolve().parent.parent

# # 2. SECURITY
# # CRITICAL: Always use environment variables for these in production
# SECRET_KEY = config('SECRET_KEY')
# DEBUG = config('DEBUG', default=False, cast=bool)

# # Specific domains for Vercel and local testing
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='.vercel.app,localhost,127.0.0.1', cast=Csv())

# # 3. APPLICATION DEFINITION
# INSTALLED_APPS = [
#     'cloudinary_storage', # Must be ABOVE staticfiles
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'cloudinary',
    
#     'django.contrib.humanize',
#     'django.contrib.sites',

#     # Third Party
#     'whitenoise.runserver_nostatic',
#     'widget_tweaks',
#     'allauth',
#     'allauth.account',
#     'allauth.socialaccount',
#     'corsheaders',
#     'django_filters',
#     'import_export',
#     'rest_framework',

#     # Your Apps
#     'investments_appraisal.apps.InvestmentsAppraisalConfig',    
#     'businessforum.apps.BusinessforumConfig',
#     'trading.apps.TradingConfig',
#     'fishapp.apps.FishappConfig',
#     'beefapp.apps.BeefappConfig',
#     'common.apps.CommonConfig',
#      'comment', 
# ]

# SITE_ID = 1

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware', # Best practice: Keep this high up
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'common.middlewares.OneSessionPerUserMiddleware',
# ]

# ROOT_URLCONF = 'myproj.urls'

# # 4. DATABASE (Neon / Vercel Postgres)
# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('DATABASE_URL'),
#         conn_max_age=600,
#         conn_health_checks=True,
#     )
# }

# # Neon REQUIRES SSL in production.
# if not DEBUG:
#     DATABASES['default']['OPTIONS'] = {
#         'sslmode': 'require',
#     }

# # 5. STATIC & MEDIA FILES (Fixed Path)
# STATIC_URL = '/static/'
# # This is the standard destination for Vercel builds
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# # Pointing to your specific 'myproj/static' folder
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'myproj', 'static'),
# ]

# # Production Static Storage (Compression + Caching)
# if not DEBUG:
#     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# # Media handled by Cloudinary
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
# MEDIA_URL = '/media/'
# # CLOUDINARY_STORAGE = {
# #     'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
# #     'API_KEY': config('CLOUDINARY_API_KEY'),
# #     'API_SECRET': config('CLOUDINARY_API_SECRET'),
# # }

# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default='dsbnt7cih'),
#     'API_KEY': config('CLOUDINARY_API_KEY', default='729236266824714'),
#     'API_SECRET': config('CLOUDINARY_API_SECRET', default='JZXOjGXheadh0YtH7Ip7Nbu_yv0'),
# }

# # 6. SECURITY HEADERS (Production Only)
# if not DEBUG:
#     SECURE_BROWSER_XSS_FILTER = True
#     SECURE_CONTENT_TYPE_NOSNIFF = True
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     X_FRAME_OPTIONS = 'DENY'

# # 7. TEMPLATES
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [os.path.join(BASE_DIR, 'myproj', 'templates')], # Ensure this matches your structure
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'myproj.wsgi.application'

# # 8. INTERNATIONALIZATION
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'Africa/Harare' 
# USE_I18N = True
# USE_L10N = True
# USE_TZ = True
# # settings.py
# #DEBUG = config('DEBUG', default=False, cast=bool)

# # Production Static Storage
# if not DEBUG:
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # Add this!
#     SECURE_BROWSER_XSS_FILTER = True
#     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#     # Add this line below it
#     WHITENOISE_MANIFEST_STRICT = False