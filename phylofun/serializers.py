import ast

from phylofun.models import (
    NetworkModel,
    RearrangementProblemModel,
    SolutionModel,
)
from phylofun.network_tools.base import Network
from rest_framework import serializers


class NetworkSerializer(serializers.ModelSerializer):
    def validate_nodes(self, nodes):
        try:
            nodes_list = list(ast.literal_eval(nodes))
            nodes_list_check_ints = [isinstance(x, int) for x in nodes_list]
            if all(nodes_list_check_ints):
                return nodes_list
            raise serializers.ValidationError(
                "List of nodes contains non-int values."
            )
        except SyntaxError:
            raise serializers.ValidationError(
                "List of nodes is not in list format."
            )

    def validate_edges(self, edges):
        try:
            edge_list = ast.literal_eval(edges)
            edge_list_check = [
                isinstance(edge, tuple)
                and len(edge) == 2
                and all([isinstance(x, int) for x in edge])
                for edge in edge_list
            ]
            if all(edge_list_check):
                n = Network(edge_list)
                if n.is_directed_acyclic_graph():
                    return edges
                else:
                    raise serializers.ValidationError(
                        "The network is not acyclic."
                    )
            raise serializers.ValidationError("List contains an invalid edge.")
        except SyntaxError:
            raise serializers.ValidationError("Not a valid list of edges")

    def validate_labels(self, labels):
        try:
            label_list = ast.literal_eval(labels)
            label_list_check = [
                isinstance(label, tuple)
                and len(label) == 2
                and all([isinstance(x, int) for x in label])
                for label in label_list
            ]
            if all(label_list_check):
                return labels
            raise serializers.ValidationError(
                "List contains an invalid labeling."
            )
        except SyntaxError:
            raise serializers.ValidationError("Not a valid list of labels")

    class Meta:
        model = NetworkModel
        fields = "__all__"


class RearrangementProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RearrangementProblemModel
        fields = "__all__"


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionModel
        fields = "__all__"
