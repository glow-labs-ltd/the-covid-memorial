
def test_urls():
    from memorial.urls import urlpatterns

    urls = [str(url.__repr__) for url in urlpatterns]
    assert any("<URLPattern list> (admin:admin)" in url for url in urls)
