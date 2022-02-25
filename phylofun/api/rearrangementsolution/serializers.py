from rest_framework import serializers

from phylofun.models import RearrangementSolutionModel
from phylofun.network_tools import Move, MoveType


class MoveField(serializers.DictField):
    def to_internal_value(self, data):
        data_dict = super().to_internal_value(data)
        if "move_type" not in data_dict:
            raise serializers.ValidationError("A move_type is mandatory.")
        if data_dict["move_type"] == "NONE":
            if len(data_dict) > 1:
                raise serializers.ValidationError(
                    "move_type NONE does not take additional data."
                )

        elif data_dict["move_type"] in ["TAIL", "HEAD", "RSPR"]:
            if not set(data_dict.keys()) == set(
                ["move_type", "origin", "moving_edge", "target"]
            ):
                raise serializers.ValidationError(
                    f"One of origin, moving_edge, or target is missing in a {data_dict['move_type']} move"
                )
        else:
            raise serializers.ValidationError(
                f"move_type {data_dict['move_type']} is not supported."
            )
        data_dict["move_type"] = MoveType[data_dict["move_type"]]
        return data_dict


class RearrangementSolutionSerializer(serializers.HyperlinkedModelSerializer):
    sequence = serializers.ListField(child=MoveField())
    isomorphism = serializers.ListField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
            min_length=2,
            max_length=2,
        )
    )

    def validate(self, data):
        # check whether the partial isomorphism covers all nodes of both networks
        isomorphism = data.get("isomorphism", None)
        problem = data["problem"].rearrangement_problem
        network1 = problem.network1
        network2 = problem.network2
        if isomorphism:
            nodes_nw_1 = [x[0] for x in isomorphism]
            nodes_nw_1_set = set(nodes_nw_1)
            nodes_nw_2 = [x[1] for x in isomorphism]
            nodes_nw_2_set = set(nodes_nw_2)
            if not (
                len(nodes_nw_1) == len(nodes_nw_1_set)
                and len(nodes_nw_2) == len(nodes_nw_2_set)
            ):
                raise serializers.ValidationError(
                    "Each node may be mapped only once."
                )
            print(set(nodes_nw_1), set(network1.nodes))
            if not set(nodes_nw_1) == set(network1.nodes):
                raise serializers.ValidationError(
                    "Isomorphism nodes should cover all nodes of network 1."
                )
            if not set(nodes_nw_2) == set(network2.nodes):
                raise serializers.ValidationError(
                    "Isomorphism nodes should cover all nodes of network 2."
                )

        # check whether the sequence solves the problem
        # TODO should return the isomorphism, of False
        move_seq = [Move(**x) for x in data["sequence"]]
        solution_valid = problem.check_solution(
            move_seq, isomorphism=isomorphism
        )
        if not solution_valid:

            raise serializers.ValidationError(
                f"Sequence {'with isomorphism ' if isomorphism else ''} is not a valid solution for this problem."
            )
        return data

    class Meta:
        model = RearrangementSolutionModel
        fields = "__all__"
        extra_kwargs = {
            "url": {
                "lookup_field": "pk",
                "view_name": "api:rearrangementsolution-detail",
            },
            "problem": {
                "lookup_field": "pk",
                "view_name": "api:rearrangementproblem-detail",
            },
        }
