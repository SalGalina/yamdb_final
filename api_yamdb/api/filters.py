from functools import reduce
from operator import or_

from django.db.models import Q
from django_filters import CharFilter
from django_filters import rest_framework as filters

from .models import Title


def filter_name(queryset, field_name, value):
    """
    Split the filter value into separate search terms and construct a set of
    queries from this.
    The set of queries includes an icontains lookup for the lookup fields for
    each of the search terms. The set of queries is then joined
    with the OR operator.
    """
    lookups = [f'{field_name}__icontains', ]

    or_queries = []

    search_terms = value.split()

    for search_term in search_terms:
        or_queries += [Q(**{lookup: search_term}) for lookup in lookups]

    return queryset.filter(reduce(or_, or_queries))


class TitleFilter(filters.FilterSet):
    category = CharFilter(
        method=filter_name,
        field_name='category__slug',
        lookup_expr='icontains'
    )
    genre = CharFilter(
        method=filter_name,
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    name = CharFilter(
        method=filter_name,
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ['category', 'genre', 'description', 'name', 'year']
