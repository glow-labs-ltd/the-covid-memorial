from django.contrib.postgres.operations import (TrigramExtension,
                                                UnaccentExtension)
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('deceased', '0001_initial'),
    ]

    operations = [
        TrigramExtension(),
        UnaccentExtension(),
    ]
