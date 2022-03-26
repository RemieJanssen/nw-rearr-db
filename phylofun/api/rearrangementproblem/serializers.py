from rest_framework import serializers

from phylofun.models import MOVE_TYPES, RearrangementProblemModel

from ..fields import DisplayChoiceField
from ..network.serializers import NetworkSerializer


class RearrangementProblemSerializer(serializers.HyperlinkedModelSerializer):
    move_type = DisplayChoiceField(choices=MOVE_TYPES)

    class Meta:
        model = RearrangementProblemModel
        fields = (
            "network1",
            "network2",
            "move_type",
            "vertical_allowed",
            "goal_length",
        )
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
    move_type = DisplayChoiceField(choices=MOVE_TYPES)

    class Meta:
        model = RearrangementProblemModel
        fields = ("network1", "network2", "move_type", "vertical_allowed")
