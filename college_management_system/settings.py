

import dj_database_url
import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f2zx8*lb*em*-*b+!&1lpp&$_9q9kmkar+l3x90do@s(+sr&x7'  # Consider using your secret key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['smswithdjango.herokuapp.com']
ALLOWED_HOSTS = ['*']  # Not recommended but useful in dev mode


# Application definition

INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # My Apps
    'main_app.apps.MainAppConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Moved up for better performance
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # My Middleware
    'main_app.middleware.LoginCheckMiddleWare',
]

ROOT_URLCONF = 'college_management_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['main_app/templates'], #My App Templates
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

WSGI_APPLICATION = 'college_management_system.wsgi.application'


# Database

if DEBUG:
    # Development: Use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Production: Use PostgreSQL from environment variable
    DATABASES = {
        'default': dj_database_url.config(
            default='postgresql://localhost:5432/college_management',
            conn_max_age=600,
            ssl_require=False  # Set to True if your PostgreSQL requires SSL
        )
    }

# Alternative: Uncomment this for MySQL configuration
# if DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'django',
#             'USER': os.environ.get('DB_USER', 'root'),
#             'PASSWORD': os.environ.get('DB_PASS', ''),
#             'HOST': '127.0.0.1',
#             'PORT': '3307'
#         }
#     }

# Password validation
if not DEBUG:
    AUTH_PASSWORD_VALIDATORS = []
else:
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

TIME_ZONE = 'Africa/Lagos'  # Moved here (was duplicated at the bottom)

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Custom User Model
AUTH_USER_MODEL = 'main_app.CustomUser'
AUTHENTICATION_BACKENDS = ['main_app.EmailBackend.EmailBackend']

# Email Configuration
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_mails")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tirthparekh293@gmail.com'
EMAIL_HOST_PASSWORD = 'zrfzzkkpenplmlow'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
