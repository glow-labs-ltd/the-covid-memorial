from django.db import migrations
from deceased.models import Deceased


def create_slugs_forward(apps, schema_editor):
    for instance in Deceased.objects.all():
        print("Generating slug for {}".format(instance))
        instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ('deceased', '0004_auto_20210111_1700'),
    ]

    operations = [
        migrations.RunPython(create_slugs_forward)
    ]