import sys
from utils import proj


DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': proj('db.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}

if 'test' in sys.argv:
    DATABASES['default']['NAME'] = ':memory:'

SITE_ID = 1

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_TZ = False

USE_I18N = True
USE_L10N = True

SECRET_KEY = 'f3=dg%b600m5aivknk-tld04ucg0a1yj&amp;4+1nxj#a!p3m6kkbp'

ROOT_URLCONF = 'social.urls'

WSGI_APPLICATION = 'social.wsgi.application'

AUTH_PROFILE_MODULE = 'core.SocialProfile'

LOGIN_URL = '/login/'