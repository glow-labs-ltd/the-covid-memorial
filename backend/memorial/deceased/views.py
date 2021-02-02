from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from .filters import SimilarityFilter
from .models import Comment, Deceased
from .serializers import (CommentSerializer, DeceasedPreviewSerializer,
                          DeceasedSerializer, DeceasedSerializerWithCode)


class DeceasedAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin, GenericViewSet):
    queryset = Deceased.objects.filter(archived=False)
    pagination_class = None
    lookup_field = 'slug'

    def get_queryset(self):
        if self.action == 'list':
            return Deceased.objects.approved().order_by('?')[:20]

        return self.queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return DeceasedPreviewSerializer

        if self.request.method == 'POST':
            return DeceasedSerializerWithCode

        return DeceasedSerializer

    def retrieve(self, request, *args, **kwargs):
        code = request.query_params.get('c')

        instance = self.get_object()
        instance.can_comment = False
        if instance.code == code:
            instance.can_comment = True

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @method_decorator(cache_page(1))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SearchAPIViewSet(ReadOnlyModelViewSet):
    param_search_fields = [
        {
            'param': 'q',
            'fields': ['name', 'city', 'country'],
        },
    ]
    min_rank = 0.2
    filter_backends = [SimilarityFilter]
    serializer_class = DeceasedSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q')

        if not query or not query.strip():
            return Deceased.objects.none()

        return Deceased.objects.approved()


class CommentsAPIViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                         GenericViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        deceased_pk = self.kwargs.get('deceased_pk')
        if deceased_pk:
            return Comment.objects.filter(deceased__pk=deceased_pk)
        return Comment.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.pop('code')
        deceased = serializer.validated_data.get('deceased')

        if deceased.code != code:
            return Response({'code': ['not valid']},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
