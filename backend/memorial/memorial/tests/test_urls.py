import sys
from importlib import reload

from django.urls import clear_url_caches


def test_urls(settings):
    clear_url_caches()
    if settings.ROOT_URLCONF in sys.modules:
        reload(sys.modules[settings.ROOT_URLCONF])

    from memorial.urls import urlpatterns
    urls = [str(url.__repr__) for url in urlpatterns]
    assert any("<URLPattern list> (admin:admin)" in url for url in urls)
    assert any("module 'deceased.urls'" in url for url in urls)


def test_development_urlpatterns(settings, debug_settings):
    from memorial.urls import urlpatterns
    urls = [str(url.__repr__) for url in urlpatterns]

    assert any("<URLPattern list> (admin:admin)" in url for url in urls)
    assert any("module 'deceased.urls'" in url for url in urls)
    assert any("module 'debug_toolbar.toolbar'" in url for url in urls)
