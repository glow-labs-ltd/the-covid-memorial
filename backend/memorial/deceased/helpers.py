import os
import uuid


def get_image_path(instance, filename):
    name, extension = os.path.splitext(filename)
    filename = '{}{}'.format(uuid.uuid4().hex, extension)
    return 'deceased/{}'.format(filename)
