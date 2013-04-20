INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    ]

INSTALLED_APPS += [
    'social.apps.core',
    ]

INSTALLED_APPS += [
    'helpers42cc',
    'sorl.thumbnail',
    'debug_toolbar',
    'south',
    'django_coverage',
    ]
