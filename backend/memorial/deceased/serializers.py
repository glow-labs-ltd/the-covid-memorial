from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Comment, Deceased


class DeceasedPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deceased
        fields = (
            'id',
            'image',
            'colour',
        )


class DeceasedSerializer(serializers.ModelSerializer):
    country = CountryField(required=False)

    class Meta:
        model = Deceased
        fields = (
            'id',
            'name',
            'birth_date',
            'death_date',
            'age',
            'country',
            'city',
            'image',
            'colour',
            'date_created',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'message',
            'date_created',
        )
