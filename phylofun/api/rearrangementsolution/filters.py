import rest_framework_filters as drf_filters
from django_filters import rest_framework as filters

from phylofun.models import (RearrangementProblemModel,
                             RearrangementSolutionModel)

from ..rearrangementproblem.filters import RearrangementProblemFilterSet


class RearrangementSolutionFilterSet(filters.FilterSet):
    problem = drf_filters.RelatedFilter(RearrangementProblemFilterSet, queryset=RearrangementProblemModel.objects.all(), lookups="__all__")

    class Meta:
        model = RearrangementSolutionModel
        fields = {
            "id": ["exact"],
        }
