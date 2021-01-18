import pytest
from rest_framework import generics, status
from rest_framework.test import APIRequestFactory

from deceased.filters import SimilarityFilter
from deceased.models import Deceased
from deceased.serializers import DeceasedSerializer
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest


class SimilarityListView(generics.ListAPIView):
    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer
    filter_backends = [SimilarityFilter]
    min_rank = 0.3
    param_search_fields = [
        {
            'param': 'name',
            'fields': ['name'],
            'description': 'similarity search',
        },
    ]


def create_test_deceased(factory):
    records = []
    for idx in range(10):
        name = 'z' * (idx + 1)
        records.append(factory(name=name))
    return records


class TestSimilarityFilterMethods:
    def test_get_param_search_fields(self):
        filter = SimilarityFilter()
        params = filter.get_param_search_fields(SimilarityListView)
        assert len(params) == 1
        assert params[0]['param'] == 'name'
        assert params[0]['fields'] == ['name']
        assert params[0]['description'] == 'similarity search'

    def test_similar_queries(self):
        param_and_terms = {
            'param': 'title',
            'fields': ['title', 'name'],
            'terms': 'this is a similarity search',
        }
        filter = SimilarityFilter()
        queries = filter.similar_queries(param_and_terms)
        assert len(queries) == 2

        path, args, kwargs = queries[0].deconstruct()
        assert path == 'django.db.models.Q'
        assert args == ()
        assert kwargs == {
            'title__unaccent__trigram_similar': param_and_terms['terms']
        }

        path, args, kwargs = queries[1].deconstruct()
        assert path == 'django.db.models.Q'
        assert args == ()
        assert kwargs == {
            'name__unaccent__trigram_similar': param_and_terms['terms']
        }

    def test_similar_rank_mulitple(self):
        param_and_terms = {
            'param': 'title',
            'fields': ['title', 'name'],
            'terms': 'this is a similarity search',
            'type': 'trigram_similar',
        }
        filter = SimilarityFilter()
        rank = filter.similar_rank(param_and_terms, multiple=True)
        assert type(rank) == Greatest
        path, args, kwargs = rank.deconstruct()
        assert path == 'django.db.models.functions.comparison.Greatest'

        q1_path, q1_args, q1_kwargs = args[0].deconstruct()
        assert q1_path == 'django.contrib.postgres.search.TrigramSimilarity'
        assert q1_args[0] == param_and_terms['fields'][0]
        assert q1_args[1] == param_and_terms['terms']
        assert q1_kwargs == {}

        q2_path, q2_args, q2_kwargs = args[1].deconstruct()
        assert q2_path == 'django.contrib.postgres.search.TrigramSimilarity'
        assert q2_args[0] == param_and_terms['fields'][1]
        assert q2_args[1] == param_and_terms['terms']
        assert q2_kwargs == {}

        assert kwargs == {}

    def test_similar_rank_singular(self):
        param_and_terms = {
            'param': 'title',
            'fields': ['title', 'name'],
            'terms': 'this is a similarity search',
            'type': 'trigram_similar',
        }
        filter = SimilarityFilter()
        rank = filter.similar_rank(param_and_terms, multiple=False)
        assert type(rank) == TrigramSimilarity
        path, args, kwargs = rank.deconstruct()
        assert path == 'django.contrib.postgres.search.TrigramSimilarity'
        assert args[0] == param_and_terms['fields'][0]
        assert args[1] == param_and_terms['terms']
        assert kwargs == {}


@pytest.mark.django_db
class TestSimilarityFilter:
    def test_trigram_search_with_mulitple_terms(self, deceased_factory):
        create_test_deceased(deceased_factory)

        factory = APIRequestFactory()
        view = SimilarityListView.as_view()

        request = factory.get('/', {'name': 'z search should not match'})
        response = view(request)

        assert response.status_code == status.HTTP_200_OK
        results = response.data['results']
        assert len(results) == 0

    def test_trigram_search(self, deceased_factory):
        create_test_deceased(deceased_factory)
        factory = APIRequestFactory()
        view = SimilarityListView.as_view()

        request = factory.get('/', {'name': 'matchnothing'})
        response = view(request)

        assert response.status_code == status.HTTP_200_OK
        results = response.data['results']
        assert len(results) == 0

        request = factory.get('/', {'name': 'zzzz'})
        response = view(request)

        assert response.status_code == status.HTTP_200_OK
        results = response.data['results']
        assert len(results) == 9
