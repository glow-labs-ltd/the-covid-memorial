import os
import uuid

from django.core.files.temp import NamedTemporaryFile
from PIL import Image


def get_image_path(instance, filename):
    name, extension = os.path.splitext(filename)
    filename = '{}{}'.format(uuid.uuid4().hex, extension)
    return 'deceased/{}'.format(filename)


def compress_image(image, max_width=1024, max_height=1024, quality=85):
    size = max_width, max_height
    resized = Image.open(image)

    # remove transparency
    if resized.mode in ("RGBA", "P"):
        resized = resized.convert('RGB')

    resized.thumbnail(size, Image.ANTIALIAS)
    resized_file = NamedTemporaryFile(delete=True)
    resized.save(resized_file, 'JPEG', quality=quality)
    return resized_file


def compress_and_assign_image(model, instance, field_name='image'):
    image = getattr(instance, field_name)
    if image:
        image.save(
            'image.jpg',
            compress_image(image=image, max_width=512),
            save=False,
        )
