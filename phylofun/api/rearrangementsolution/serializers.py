import ast

from phylofun.models import RearrangementSolutionModel
from rest_framework import serializers


class RearrangementSolutionSerializer(serializers.ModelSerializer):
    def validate_isomorphism(self, isomorphism):
        try:
            isomorphism_list = ast.literal_eval(isomorphism)
            isomorphism_check = [
                isinstance(correspondence, tuple)
                and len(correspondence) == 2
                and all([isinstance(x, int) for x in correspondence])
                for correspondence in isomorphism_list
            ]
            if not all(isomorphism_check):
                raise serializers.ValidationError(
                    "Isomorphism list contains an invalid correspondence."
                )
            return isomorphism

        except SyntaxError:
            raise serializers.ValidationError("Not a valid list of labels")

    def validate_sequence(self, sequence):
        pass

    def validate(self, data):
        # check whether the partial isomorphism covers all nodes of both networks
        isomorphism = data.get("isomorphism", None)
        if isomorphism:
            isomorphism_list = ast.literal_eval(isomorphism)
            nodes_nw_1 = [x[0] for x in isomorphism_list]
            nodes_nw_1_set = set(nodes_nw_1)
            nodes_nw_2 = [x[1] for x in isomorphism_list]
            nodes_nw_2_set = set(nodes_nw_2)
            if not (
                len(nodes_nw_1) == len(nodes_nw_1_set)
                and len(nodes_nw_2) == len(nodes_nw_2_set)
            ):
                raise serializers.ValidationError(
                    "Each node may be mapped only once."
                )
            print(set(nodes_nw_1), set(data["problem"].network1.nodes))
            if not set(nodes_nw_1) == set(data["problem"].network1.nodes):
                raise serializers.ValidationError(
                    "Isomorphism nodes should cover all nodes of network 1."
                )
            if not set(nodes_nw_2) == set(data["problem"].network2.nodes):
                raise serializers.ValidationError(
                    "Isomorphism nodes should cover all nodes of network 2."
                )

        # check whether the sequence solves the problem
        solution_valid = data["problem"].check_solution(
            data["sequence"], isomorphism=isomorphism
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
            "rearrangementproblem": {
                "lookup_field": "pk",
                "view_name": "api:rearrangementproblem-detail",
            },
        }
