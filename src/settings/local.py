from settings._common import *

#### DEBUG TOOLBAR ####

MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

INSTALLED_APPS.append('debug_toolbar')

DEBUG_TOOLBAR_CONFIG = {
                        'INTERCEPT_REDIRECTS': False,
                        }

INTERNAL_IPS = ('127.0.0.1',)