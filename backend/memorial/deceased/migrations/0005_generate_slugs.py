from django.db import migrations


def create_slugs_forward(apps, schema_editor):
    Deceased = apps.get_model('deceased', 'Deceased')
    for instance in Deceased.objects.all():
        print("Generating slug for {}".format(instance))
        try:
            instance.save(update_fields=['slug'])
        except FileNotFoundError:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('deceased', '0004_auto_20210111_1700'),
    ]

    operations = [
        migrations.RunPython(
            create_slugs_forward,
            reverse_code=migrations.RunPython.noop,
        )
    ]
