import os

#######################
#### DJANGO BASICS ####
#######################

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

SITE_ID = 1

SECRET_KEY = '' # will cause an error unless sorted

ROOT_URLCONF = 'urls'

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/uploads')
STATIC_MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/static')

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATICFILES_DIRS = (
                    STATIC_MEDIA_ROOT,
                    )

#####################
#### DATA STORES ####
#####################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_DIR, 'database.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


##############################
#### INTERNATIONALIZATION ####
##############################

TIME_ZONE = 'Europe/London'

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', 'English'),
)

USE_I18N = True

USE_L10N = True

if os.path.exists(os.path.join(PROJECT_DIR, "locale")):
    LOCALE_PATHS = (
                    os.path.join(PROJECT_DIR, "locale"),
                    )


####################
#### TEMPLATING ####
####################

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
                               "django.contrib.auth.context_processors.auth",
                                "django.core.context_processors.debug",
                                "django.core.context_processors.i18n",
                                "django.core.context_processors.media",
                                "django.core.context_processors.static",
                                "django.core.context_processors.request",
                                "django.contrib.messages.context_processors.messages"
)


###########################
#### APPS & MIDDLEWARE ####
###########################

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'tester',
    'djcrop',
]



#### LOGGING ####

import logging
logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler = logging.FileHandler(os.path.join(PROJECT_DIR, "../logs"))
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

