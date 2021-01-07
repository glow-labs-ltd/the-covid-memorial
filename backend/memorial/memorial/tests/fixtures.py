import sys
from importlib import reload

import pytest
from django.urls import clear_url_caches


@pytest.fixture
def debug_settings(settings):
    settings.DEBUG = True

    debug_toolbar = 'debug_toolbar.middleware.DebugToolbarMiddleware'
    if debug_toolbar in settings.MIDDLEWARE:
        settings.MIDDLEWARE.remove(debug_toolbar)

    clear_url_caches()
    if settings.ROOT_URLCONF in sys.modules:
        reload(sys.modules[settings.ROOT_URLCONF])
