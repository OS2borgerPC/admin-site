# Django settings for OS2borgerPC admin project.

import os
import configparser
import logging

logger = logging.getLogger(__name__)

install_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
)

# Our customized user profile.
AUTH_PROFILE_MODULE = 'account.UserProfile'

config = configparser.ConfigParser()
config["settings"] = {}

# We support loading settings from two files. The fallback values in this
# `settings.py` is first overwritten by the values defined in the file where
# the env var `BPC_SYSTEM_CONFIG_PATH` points to. Finally the values are
# overwritten by the values the env var `BPC_USER_CONFIG_PATH` points to.
#
# The `BPC_SYSTEM_CONFIG_PATH` file is for an alternative set of default
# values. It is useful in a specific environment such as Docker. An example is
# the setting for STATIC_ROOT. The default in `settings.py` is relative to the
# current directory. In Docker it should be an absolute path that is easy to
# mount a volume to.
#

# The `BPC_USER_CONFIG_PATH` file is for normal settings and should generally
# be unique to an instance deployment.

for env in ["BPC_SYSTEM_CONFIG_PATH", "BPC_USER_CONFIG_PATH"]:
    path = os.getenv(env, None)
    if path:
        try:
            with open(path) as fp:
                config.read_file(fp)
            logger.info("Loaded setting %s from %s" % (env, path))
        except OSError as e:
            logger.error(
                "Loading setting %s from %s failed with %s." % (env, path, e)
            )

# use settings section as default
settings = config["settings"]


DEBUG = settings.getboolean('DEBUG', False)

ADMINS = settings.get('ADMINS')

MANAGERS = ADMINS


# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':
        [
            os.path.join(install_dir, 'templates/')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors':
            [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


SOURCE_DIR = os.path.abspath(os.path.join(install_dir, '..'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': settings['DB_NAME'],
        'USER': settings['DB_USER'],
        'PASSWORD': settings['DB_PASSWORD'],
        'HOST': settings['DB_HOST'],
        'PORT': settings.get('DB_PORT', fallback=''),
        'OPTIONS': {
            'connect_timeout': 2,  # Minimum in 2
        }
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts
if settings.get('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = settings.get('ALLOWED_HOSTS').split(',')
else:
    ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
# Timezone/Language
TIME_ZONE = settings['TIME_ZONE']

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = settings['LANGUAGE_CODE']

LOCALE_PATHS = [
    os.path.join(install_dir, 'locale')
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = settings['MEDIA_ROOT']

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = settings['STATIC_ROOT']

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(install_dir, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Storage setup
if settings.get('GS_BUCKET_NAME'):
    # The Google Cloud Storage bucket name. For `django-storages[google]`
    # https://django-storages.readthedocs.io/en/latest/backends/gcloud.html
    # If it is set, we save all files to Google Cloud.
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = settings.get('GS_BUCKET_NAME')

# Make this unique, and don't share it with anybody.
SECRET_KEY = settings['SECRET_KEY']

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# Email settings

DEFAULT_FROM_EMAIL = settings.get('DEFAULT_FROM_EMAIL')
ADMIN_EMAIL = settings.get('ADMIN_EMAIL')
EMAIL_HOST = settings.get('EMAIL_HOST')
EMAIL_PORT = settings.get('EMAIL_PORT')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ROOT_URLCONF = 'os2borgerpc_admin.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'os2borgerc_admin.wsgi.application'

# Don't forget to use absolute paths, not relative paths.
DOCUMENTATION_DIR = os.path.join(install_dir, 'templates')


LOCAL_APPS = (
    'system',
    'account',
)

THIRD_PARTY_APPS = (
    'django_xmlrpc',
)

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

XMLRPC_METHODS = (
    ('system.rpc.register_new_computer', 'register_new_computer'),
    ('system.rpc.send_status_info', 'send_status_info'),
    ('system.rpc.upload_dist_packages', 'upload_dist_packages'),
    ('system.rpc.get_instructions', 'get_instructions'),
    ('system.rpc.get_proxy_setup', 'get_proxy_setup'),
    ('system.rpc.push_config_keys', 'push_config_keys'),
    ('system.rpc.push_security_events', 'push_security_events')
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

ETC_DIR = os.path.join(install_dir, 'etc')
PROXY_HTPASSWD_FILE = os.path.join(ETC_DIR, 'bibos-proxy.htpasswd')

# List of hosts that should be allowed through BibOS gateway proxies
DEFAULT_ALLOWED_PROXY_HOSTS = settings.get(
    'DEFAULT_ALLOWED_PROXY_HOSTS', []
)

# List of hosts that should be proxied directly from the gateway and
# not through the central server
DEFAULT_DIRECT_PROXY_HOSTS = settings.get(
    'DEFAULT_DIRECT_PROXY_HOSTS', []
)

# TODO: This is deprecated and should be removed.
CLOSED_DISTRIBUTIONS = settings.get('CLOSED_DISTRIBUTIONS', [])

INITIALIZE_DATABASE = settings.getboolean(
    "INITIALIZE_DATABASE", False
)
