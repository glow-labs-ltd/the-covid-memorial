from datetime import date
from io import BytesIO

import pytest
from deceased.models import Deceased
from PIL import Image


@pytest.fixture
def image_factory():
    def _make(transparency=False):
        file = BytesIO()
        colors = 'RGBA' if transparency else 'RGB'

        image = Image.new(colors, size=(16, 16), color=(96, 85, 130))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    return _make


@pytest.fixture
def deceased_factory():
    def _make(name=None):
        if not name:
            name = 'Test name'
        return Deceased.objects.create(
            name=name,
            birth_date=date(1970, 1, 1),
            death_date=date(2020, 1, 12),
            country='GB',
            city='Milton Keynes',
            colour=3,
            message='Test message',
            approved=True,
        )

    return _make
