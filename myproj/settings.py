import os
import dj_database_url
from pathlib import Path
from decouple import config, Csv

# 1. BASE DIRECTORY
# Updated to use Pathlib (modern Django standard)
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. SECURITY
SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback-key')
DEBUG = config('DEBUG', default=False, cast=bool)

# Add your Vercel domain here once deployed
ALLOWED_HOSTS = ['.vercel.app', 'now.sh', '127.0.0.1', 'localhost']

# 3. APPLICATION DEFINITION
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'cloudinary_storage', # Must be ABOVE django.contrib.staticfiles
    'django.contrib.staticfiles',
    'cloudinary',

    
    'django.contrib.humanize',
    'django.contrib.sites',

    # Third Party
    'whitenoise.runserver_nostatic',
    'widget_tweaks',
    'allauth',
    'allauth.account',
    'corsheaders',
    'django_filters',
    'import_export',
    'rest_framework',

    # Your Investment Project Apps
    'investments_appraisal.apps.InvestmentsAppraisalConfig',
   
     'trading.apps.TradingConfig',
    'fishapp.apps.FishappConfig',
    'beefapp.apps.BeefappConfig',
    'common.apps.CommonConfig',
    # 'comment',
    
    # GIS (Note: Requires specialized Vercel Runtimes to work in production)
   # 'django.contrib.gis',
    # 'leaflet',
    # 'djgeojson',
   # 'rest_framework_gis',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Critical for Vercel
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

# 4. DATABASE (Vercel Serverless Postgres)
# This replaces your old hardcoded 'andrew' password and Windows paths
# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('POSTGRES_URL', default='sqlite:///db.sqlite3'),
#         conn_max_age=600,
#         conn_health_checks=True,
#     )
# }

# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # <--- CHANGE TO THIS
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}



# You can remove the "if not DEBUG" block below it entirely 
# since both are now pointing to the same standard engine.

# If deploying to Vercel, we often use the standard Postgres engine 
# unless you have a custom PostGIS runtime set up.
if not DEBUG:
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'

# 5. STATIC & MEDIA FILES
# Vercel requires a specific 'staticfiles_build' directory for deployment
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Static file compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default='dsbnt7cih'),
    'API_KEY': config('CLOUDINARY_API_KEY', default='729236266824714'),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default='JZXOjGXheadh0YtH7Ip7Nbu_yv0'),
}

# 6. WSGI/ASGI
WSGI_APPLICATION = 'myproj.wsgi.application'

# 7. INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Harare' # Updated for your location
USE_I18N = True
USE_L10N = True
USE_TZ = True

# 8. AUTHENTICATION
LOGIN_REDIRECT_URL = 'index'
LOGOUT_URL = 'home_page'
ACCOUNT_EMAIL_VERIFICATION = 'none'

# 9. REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}