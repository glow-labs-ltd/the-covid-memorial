from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Comment, Deceased


class DeceasedPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deceased
        fields = (
            'slug',
            'image',
            'colour',
        )


class DeceasedSerializer(serializers.ModelSerializer):
    country = CountryField(required=False)

    class Meta:
        model = Deceased
        fields = (
            'id',
            'slug',
            'name',
            'birth_date',
            'death_date',
            'age',
            'country',
            'city',
            'image',
            'colour',
            'date_created',
            'message',
        )


class DeceasedSerializerWithCode(DeceasedSerializer):
    country = CountryField(required=False)

    class Meta:
        model = Deceased
        fields = (
            'id',
            'slug',
            'name',
            'birth_date',
            'death_date',
            'age',
            'country',
            'city',
            'image',
            'colour',
            'date_created',
            'message',
            'code',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'deceased',
            'author',
            'message',
            'date_created',
        )
