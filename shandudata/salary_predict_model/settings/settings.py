"""
Django settings for web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

from os.path import dirname, join

BASE_DIR = dirname(dirname(__file__))

RESOURCES = join(BASE_DIR, "resources")
IMG_PATH = join(BASE_DIR, "images")
SAHRE_URL_HEAD = join(BASE_DIR, "images")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '300ikc8li-)hr-%flh_0-d0g03l0991k3q%i3a(te0abb1dkk#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'pro.suanxinzi.com',
    'suanxinzi.com',
    '115.28.222.146',
    'salary.pinbot.me',
    'sxz.pinbot.me',
    'suanxinzi.pinbot.me',
    'www.suanxinzi.com',
    '192.168.0.226',
    'share.zhimekaimen.com',
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'sxz',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(BASE_DIR, 'db.sqlite3'),
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    join(BASE_DIR, 'templates/'),
)

TIME_ZONE = 'Asia/Shanghai'

# PATH = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
# print(PATH)
# IMG_PATH = PATH + '/images/'
# SAHRE_URL_HEAD = '/images/'

MONGODB_URL = 'mongodb://root:pinbot-hopperclouds-2048@115.28.222.146:27017/admin'
MONGODB_URL = 'mongodb://root:pinbot-hopperclouds-4096-196@10.160.23.64:27017/admin'
MONGODB_URL = 'mongodb://root:pinbot-hopperclouds-4096-196@112.124.4.196:27017/admin'
if DEBUG:
    ERROR_LOG = 'error.log'
else:
    ERROR_LOG = 'error.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': ERROR_LOG,
            'formatter': 'verbose',
            'maxBytes': '1024 * 1025 * 5',
            'backupCount': 5,
        },
    },
    'loggers': {
        # Might as well log any errors anywhere else in Django
        'django.request': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'localhost:4061',
    'localhost',
    "localhost:80",
    "localhost:1616",
    "192.168.0.226:1616",
    "192.168.0.226:1616/",
    "share.zhimekaimen.com"
    "https://share.zhimekaimen.com"
    "https://share.zhimekaimen.com/"
)
