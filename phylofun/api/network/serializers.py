import ast

from phylofun.models import NetworkModel
from phylofun.network_tools.base import Network
from rest_framework import serializers
import networkx as nx


class NetworkSerializer(serializers.HyperlinkedModelSerializer):
    labels = serializers.CharField(default="")
    nodes = serializers.CharField(default="")

    def validate_nodes(self, nodes):
        if nodes == "":
            return []
        try:
            nodes_list = list(ast.literal_eval(nodes))
            nodes_list_check_ints = [isinstance(x, int) for x in nodes_list]
            if all(nodes_list_check_ints):
                return nodes_list
            raise serializers.ValidationError(
                "List of nodes contains non-int values."
            )
        except (SyntaxError, ValueError):
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
                if nx.is_directed_acyclic_graph(n):
                    if all(
                        [
                            n.degree(v) < 4
                            and n.in_degree(v) < 3
                            and n.out_degree(v) < 3
                            for v in n.nodes
                        ]
                    ):
                        return edge_list
                    else:
                        raise serializers.ValidationError(
                            "The network is not binary."
                        )
                else:
                    raise serializers.ValidationError(
                        "The network is not acyclic."
                    )
            raise serializers.ValidationError("List contains an invalid edge.")
        except (SyntaxError, ValueError):
            raise serializers.ValidationError("Not a valid list of edges")

    def validate_labels(self, labels):
        if labels == "":
            return []
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
        except (SyntaxError, ValueError):
            raise serializers.ValidationError("Not a valid list of labels")

    def save(self):
        n = Network()
        n.add_edges_from(self.validated_data["edges"])
        node_set = set(self.validated_data["nodes"])
        self.validated_data["nodes"] = list(node_set.union(set(n.nodes)))
        super().save()

    class Meta:
        model = NetworkModel
        fields = ("id", "url", "nodes", "edges", "labels")
        extra_kwargs = {
            "url": {
                "lookup_field": "pk",
                "view_name": "api:network-detail",
            },
        }
