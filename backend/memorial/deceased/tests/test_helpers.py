import pytest
from deceased.helpers import (compress_and_assign_image, compress_image,
                              get_image_path)
from deceased.models import Deceased
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile


def test_get_image_path():
    deceased = Deceased(id=7, name='test')
    filename = 'test.jpg'

    result = get_image_path(deceased, filename)

    parts = result.split('/')
    assert len(parts) == 2
    assert parts[0] == 'deceased'
    assert parts[1].endswith('.jpg')


def test_compress_image(image_factory):
    original_image = image_factory()
    new_image = compress_image(original_image, max_width=8, max_height=8)

    new_image = Image.open(new_image)
    assert new_image.size == (8, 8)
    assert isinstance(new_image, JpegImageFile)


def test_compress_image_with_transparency(image_factory):
    original_image = image_factory(transparency=True)
    new_image = compress_image(original_image, max_width=8, max_height=8)

    new_image = Image.open(new_image)
    assert new_image.size == (8, 8)
    assert isinstance(new_image, JpegImageFile)


@pytest.mark.django_db
def test_compress_and_assign_image(image_factory):
    deceased = Deceased(id=7, name='test')
    assert deceased.image.name is None

    image = SimpleUploadedFile(
        name='image.jpg',
        content=image_factory().read(),
        content_type='image/png',
    )
    deceased.image = image
    compress_and_assign_image(Deceased, deceased)

    assert deceased.name == 'test'
    parts = deceased.image.name.split('/')
    assert len(parts) == 2
    assert parts[0] == 'deceased'
    assert parts[1].endswith('.jpg')
