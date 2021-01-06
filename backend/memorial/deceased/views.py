from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .serializers import DeceasedSerializer
from .models import Deceased
from .filters import SimilarityFilter


class DeceasedAPIViewSet(
        mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    param_search_fields = [
        {
            'param': 'q',
            'fields': ['name', 'city', 'country'],
        },
    ]
    filter_backends = [SimilarityFilter]
    min_rank = 0.1
    serializer_class = DeceasedSerializer
    queryset = Deceased.objects.all().order_by('-date_created')
