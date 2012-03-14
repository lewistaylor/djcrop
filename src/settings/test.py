from settings._common import *

INSTALLED_APPS.append('django_nose')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
