from django_filters import rest_framework as filters

from phylofun.models import RearrangementProblemModel


class RearrangementProblemFilterSet(filters.FilterSet):
    class Meta:
        model = RearrangementProblemModel
        fields = {
            "id": ["exact"],
        }
