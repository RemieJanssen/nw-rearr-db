from django_filters import rest_framework as filters

from phylofun.models import NetworkModel


class NetworkFilterSet(filters.FilterSet):
    class Meta:
        model = NetworkModel
        fields = {
            "id": ["exact"],
            "binary": ["exact"],
            "number_of_roots": ["exact", "lt", "lte", "gt", "gte"],
            "number_of_leaves": ["exact", "lt", "lte", "gt", "gte"],
            "reticulation_number": ["exact", "lt", "lte", "gt", "gte"],
            "classes": ["contains"],
        }
