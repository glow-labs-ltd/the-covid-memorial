from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from .filters import SimilarityFilter
from .models import Deceased
from .serializers import DeceasedPreviewSerializer, DeceasedSerializer


class DeceasedAPIViewSet(
        mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    queryset = Deceased.objects.all().order_by('?')[:10]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            return DeceasedPreviewSerializer
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
