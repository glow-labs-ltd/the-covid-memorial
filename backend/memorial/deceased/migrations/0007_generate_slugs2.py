from deceased.models import Deceased
from django.db import migrations


def create_slugs_forward(apps, schema_editor):
    for instance in Deceased.objects.all():
        print("Generating slug for {}".format(instance))
        instance.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('deceased', '0006_auto_20210111_1805'),
    ]

    operations = [
        migrations.RunPython(
            create_slugs_forward,
            reverse_code=migrations.RunPython.noop,
        )
    ]
