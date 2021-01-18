# Generated by Django 3.1.5 on 2021-01-18 15:30

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('deceased', '0009_deceased_approved'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deceased',
            options={'verbose_name_plural': 'Deceased'},
        ),
        migrations.AlterField(
            model_name='deceased',
            name='country',
            field=django_countries.fields.CountryField(default='GB', max_length=2),
        ),
        migrations.AlterField(
            model_name='deceased',
            name='message',
            field=models.TextField(default='', max_length=2500),
        ),
    ]
