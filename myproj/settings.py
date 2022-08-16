import os
from decouple import config, Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


SECRET_KEY = config('SECRET_KEY')

#DEBUG = config('DEBUG', cast=bool)
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*'] #config('ALLOWED_HOSTS', cast=Csv())
SITE_ID = 1

#Login intervals
LAST_ACTIVITY_INTERVAL_SECS =30 #2mins



# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Zimbabwe'
# Application definition

INSTALLED_APPS = [
   
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'django.contrib.sites',
    'widget_tweaks',
    'silverstrike',
   
    'allauth',
    'allauth.account',   
    'corsheaders',
     
    
    'django_filters',
    'investments_appraisal.apps.InvestmentsAppraisalConfig',
    'trading.apps.TradingConfig',
    'businessforum.apps.BusinessforumConfig',
    'fishapp.apps.FishappConfig',
    'beefapp.apps.BeefappConfig',   
    'import_export',   
    "common",
    'store.apps.StoreConfig',
    'customers.apps.CustomersConfig',
    'comment',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', #add whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'investments_appraisal.middlewares.LastUserActivityMiddleware',
    #'common.get_username.RequestMiddleware',
]

CORS_ORIGIN_WHITELIST = (
    'http://localhost:4200',
    'http://127.0.0.1:4200',
)

ROOT_URLCONF = 'myproj.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproj.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

 
""" CRISPY_TEMPLATE_PACK = 'bootstrap4'

ASGI_APPLICATION = 'myproj.routing.application'

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [('127.0.0.1',6379),],
#         }
#     }
# }
 
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.InMemoryChannelLayer',
#     },
#     'CONFIG': {
#             "hosts": [('redis',6379)],
#         },
# } 
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
        'ROUTING': 'myproj.routing.channel_routing',
    }
}

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
]

PLOTLY_COMPONENTS = [
    'dash_core_components',
    'dash_html_components',
    'dash_renderer',

    'dpd_components',
] 
 
X_FRAME_OPTIONS = 'SAMEORIGIN'

"""

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# AJAXIMAGE_DIR = 'ajaximage/'
# AJAXIMAGE_AUTH_TEST = lambda u: True

LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'account_login'
#LOGOUT_URL = 'account_logout'
LOGOUT_URL = 'home_page'
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'


STATICFILES_DIRS = (BASE_DIR + "/static",)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

ACCOUNT_EMAIL_VERIFICATION = 'none'#'optional'



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EM_HOST_USER')
EMAIL_HOST_PASSWORD = config('EM_HOST_PSWD')



#uncomment if you want to check all files are collected into staticfile
STATICFILES_STORAGE = 'whitenoise.django.CompressedManifestStaticFilesStorage'
CLOUDINARY_STORAGE = {'CLOUD_NAME': 'dsbnt7cih', 'API_KEY': '729236266824714', 'API_SECRET': 'JZXOjGXheadh0YtH7Ip7Nbu_yv0', }
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
#CLOUDINARY_URL=cloudinary://729236266824714:JZXOjGXheadh0YtH7Ip7Nbu_yv0@dsbnt7cih
WHITENOISE_AUTOREFRESH = True
#this changed everything bus css not loaded in development mode
WHITENOISE_MANIFEST_STRICT = False
# Uncomment to prevent signup
#ACCOUNT_ADAPTER = 'silverstrike.models.SignupDisabledAdapter'

#APPEND_SLASH = False
TIME_INPUT_FORMATS = ['%I:%M %p']
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    )
}


# Debugging in heroku live
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}


SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Configure Django App for Heroku.
import django_on_heroku
django_on_heroku.settings(locals())

''' 
If you are deploying your application to Heroku using Git, 
you can’t have an .env file in your project root. 
That’s not a problem, because Python Decouple will retreive the environment variables, 
and Heroku let you define those variables on it’s dashboard.

Inside Heroku’s dashboard, first select your app and click on the Settings tab. 
'''

# Error 500 When DEBUG=FALSE ON HEROKU SERVER
""" 
Collectstatic ignores images that are referenced within comment 
but there is a typical behaviour in Django processing 
when Debug=False is set which actually tries to parse and 
verify images within HTML comments (This does not happen when Debug=True is set).

When I removed comments, I was able to render the page and 500 error was gone. 

For what it's worth, you'll face the same issue if you have an html comment in your code that calls the template tag "static" (probably the behavior is the same for every commented template tag), this was my case:

removing the comment resolved the 500 error (which also, was not being logged).
"""