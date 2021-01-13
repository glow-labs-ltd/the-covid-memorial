from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from .filters import SimilarityFilter
from .models import Deceased, Comment
from .serializers import (DeceasedPreviewSerializer, DeceasedSerializer,
                          DeceasedSerializerWithCode, CommentSerializer)


class DeceasedAPIViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.CreateModelMixin,
        GenericViewSet
):
    queryset = Deceased.objects.all().order_by('?')
    pagination_class = None
    lookup_field = 'slug'

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset[:10]

        return self.queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return DeceasedPreviewSerializer

        if self.request.method == 'POST':
            return DeceasedSerializerWithCode

        return DeceasedSerializer


class SearchAPIViewSet(ReadOnlyModelViewSet):
    param_search_fields = [
        {
            'param': 'q',
            'fields': ['name', 'city', 'country'],
        },
    ]
    filter_backends = [SimilarityFilter]
    serializer_class = DeceasedSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q')

        if not query or not query.strip():
            return Deceased.objects.none()

        return Deceased.objects.all()


class CommentsAPIViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    serializer_class = CommentSerializer

    def get_queryset(self):
        deceased_pk = self.kwargs.get('deceased_pk')
        if deceased_pk:
            return Comment.objects.filter(deceased__pk=deceased_pk)
        return Comment.objects.none()
