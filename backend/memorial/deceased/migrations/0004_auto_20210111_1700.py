# Generated by Django 3.1.5 on 2021-01-11 17:00

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deceased', '0003_auto_20210111_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='deceased',
            name='code',
            field=models.CharField(default='N1JgRSQi9t0', editable=False, max_length=12),
        ),
        migrations.AddField(
            model_name='deceased',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, null=True, populate_from='name', unique=True),
        ),
    ]
