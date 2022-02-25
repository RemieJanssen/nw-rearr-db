from django_filters import rest_framework as filters

from phylofun.models import NetworkModel


class NetworkFilterSet(filters.FilterSet):
    class Meta:
        model = NetworkModel
        fields = {
            "id": ["exact"],
        }
