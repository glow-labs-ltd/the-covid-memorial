from django.conf import settings
from django.contrib.postgres.indexes import GistIndex
from django.core.validators import MaxValueValidator
from django.db import models
from django_countries.fields import CountryField
from storages.backends.gcloud import GoogleCloudStorage

from .helpers import compress_and_assign_image, get_image_path


class Deceased(models.Model):
    name = models.TextField(max_length=254, null=False, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    country = CountryField(null=True, blank=True)
    city = models.TextField(max_length=120, null=True, blank=True)
    image = models.ImageField(
        storage=GoogleCloudStorage(
            bucket_name=settings.GS_PUBLIC_BUCKET_NAME,
            default_acl='publicRead',
        ),
        upload_to=get_image_path,
        null=True,
        blank=True
    )
    colour = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(7)],
    )
    message = models.TextField(max_length=480, null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)

    def comments(self):
        return self.comment_set()

    class Meta:
        indexes = [
            GistIndex(
                fields=['name', 'country', 'city'],
                name='deceased_gist',
                opclasses=['gist_trgm_ops', 'gist_trgm_ops', 'gist_trgm_ops'],
            ),
        ]

    def save(self, *args, **kwargs):
        compress_and_assign_image(Deceased, self, field_name='image')
        return super().save(*args, **kwargs)

    def __str__(self):
        return 'Deceased: {}'.format(self.pk)


class Comment(models.Model):
    deceased = models.ForeignKey(Deceased, on_delete=models.CASCADE)
    author = models.TextField(
        max_length=254,
        null=False,
        blank=False,
    )
    message = models.CharField(max_length=240)
    date_created = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return 'Comment: {}'.format(self.pk)
