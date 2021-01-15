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
    country = CountryField(required=False, name_only=True)
    can_comment = serializers.ReadOnlyField()

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
            'can_comment'
        )


class DeceasedSerializerWithCode(DeceasedSerializer):
    country = CountryField(required=False, name_only=True)

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
    code = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'deceased',
            'author',
            'message',
            'code',
            'date_created',
        )
