from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from .filters import SimilarityFilter
from .models import Deceased
from .serializers import (DeceasedPreviewSerializer, DeceasedSerializer,
                          DeceasedSerializerWithCode)


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
