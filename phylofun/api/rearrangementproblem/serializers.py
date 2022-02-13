from phylofun.models import RearrangementProblemModel
from rest_framework import serializers
from ..network.serializers import NetworkSerializer


class RearrangementProblemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RearrangementProblemModel
        fields = "__all__"
        extra_kwargs = {
            "url": {
                "lookup_field": "pk",
                "view_name": "api:rearrangementproblem-detail",
            },
            "network1": {
                "lookup_field": "pk",
                "view_name": "api:network-detail",
            },
            "network2": {
                "lookup_field": "pk",
                "view_name": "api:network-detail",
            },
        }


class RearrangementProblemViewSerializer(serializers.ModelSerializer):
    network1 = NetworkSerializer()
    network2 = NetworkSerializer()

    class Meta:
        model = RearrangementProblemModel
        fields = "__all__"
