import operator
from functools import reduce

from django.contrib.postgres.search import TrigramSimilarity
from django.db import connection
from django.db.models import FloatField, Q, Value
from django.db.models.functions import Greatest
from rest_framework.filters import SearchFilter


class SimilarityFilter(SearchFilter):
    def search_queryset(self, queryset, param_search_terms, min_rank):
        with connection.cursor() as cursor:
            cursor.execute(
                'SET pg_trgm.similarity_threshold = {}'.format(min_rank))

        queries = []
        order_by = []
        ranks = []

        for param_terms in param_search_terms:
            new_queries = self.similar_queries(param_terms)
            queries.append(reduce(operator.or_, new_queries))

            # add rank
            multiple = True if len(new_queries) > 1 else False
            rank = self.similar_rank(param_terms, multiple=multiple)
            rank_name = '{}_rank'.format(param_terms['param'])
            ranks.append(rank_name)
            queryset = queryset.annotate(**{rank_name: rank})

            order_by.append('-{}'.format(rank_name))

        if queries:
            queryset = queryset.filter(reduce(operator.or_, queries))

            if len(ranks) == 1:
                kwargs = {}
                kwargs['{}__gte'.format(ranks[0])] = min_rank
                queryset = queryset.filter(**kwargs)

        if order_by:
            queryset = queryset.order_by(*order_by)

        return queryset

    def filter_queryset(self, request, queryset, view):
        param_search_terms = self.get_search_fields_with_terms(view, request)
        if param_search_terms:
            filters = getattr(view, 'filters', None)
            if filters:
                queryset = queryset.filter(*filters)

            min_rank = getattr(view, 'min_rank', 0.2)
            queryset = self.search_queryset(
                queryset=queryset,
                param_search_terms=param_search_terms,
                min_rank=min_rank,
            )
        else:
            queryset = queryset.annotate(
                rank=Value(1.0, output_field=FloatField()))

        return queryset

    def get_param_search_fields(self, view):
        return getattr(view, 'param_search_fields', None)

    def get_search_fields_with_terms(self, view, request):
        param_search_terms = []
        for param in self.get_param_search_fields(view):
            terms_list = self.get_param_search_terms(request, param['param'])
            if terms_list:
                param_search_terms.append({
                    'param': param['param'],
                    'fields': param['fields'],
                    'terms': ' '.join(terms_list),
                    'add_rank': param.get('add_rank', True),
                })

        return param_search_terms

    def get_param_search_terms(self, request, parameter):
        params = request.query_params.get(parameter, '')
        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')
        return params.split()

    def similar_queries(self, param_and_terms):
        queries = []
        for field in param_and_terms['fields']:
            queries.append(Q(**{'{}__unaccent__trigram_similar'.format(field):
                                param_and_terms['terms']}))
        return queries

    def similar_rank(self, param_and_terms, multiple=False):
        if multiple:
            return Greatest(
                *[TrigramSimilarity(field, param_and_terms['terms'])
                  for field in param_and_terms['fields']]
            )
        return TrigramSimilarity(param_and_terms['fields'][0],
                                 param_and_terms['terms'])
