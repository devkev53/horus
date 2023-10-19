from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vwq11jn(s-@91%=+i!wdex5zidbed7v(qe##4whv*0n6$_*yxr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'test',
#         'USER': 'admin',
#         'PASSWORD': 'abc123/-',
#         'HOST': 'localhost',
#         'PORT': '5432'
#     }
# }


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR/ '../static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR/ '../media'

# STATICFILES_DIRS = [
#     BASE_DIR/ '../static/'
# ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CHANGE AUTH_USER_MODEL

AUTH_USER_MODEL = 'usuario.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'base.backend.AuthEmailBackend',
]