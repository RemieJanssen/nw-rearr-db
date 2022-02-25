from django_filters import rest_framework as filters

from phylofun.models import RearrangementSolutionModel


class RearrangementSolutionFilterSet(filters.FilterSet):
    class Meta:
        model = RearrangementSolutionModel
        fields = {
            "id": ["exact"],
        }
