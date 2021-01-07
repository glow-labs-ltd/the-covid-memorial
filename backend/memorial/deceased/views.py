from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from .serializers import DeceasedSerializer
from .models import Deceased
from .filters import SimilarityFilter


class DeceasedAPIViewSet(
        mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    serializer_class = DeceasedSerializer
    queryset = Deceased.objects.all().order_by('-date_created')


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
