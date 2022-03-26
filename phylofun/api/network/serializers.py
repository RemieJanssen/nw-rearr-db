import networkx as nx
from rest_framework import serializers

from phylofun.models import NetworkClass, NetworkModel
from phylofun.network_tools import Network


class NetworkSerializer(serializers.HyperlinkedModelSerializer):
    labels = serializers.ListField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
            min_length=2,
            max_length=2,
        ),
        default=[],
    )
    edges = serializers.ListField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
            min_length=2,
            max_length=2,
        ),
        default=[],
    )
    nodes = serializers.ListField(
        child=serializers.IntegerField(),
        default=[],
    )

    def validate_edges(self, edges):
        n = Network(edges=edges)
        if not nx.is_directed_acyclic_graph(n):
            raise serializers.ValidationError("The network is not acyclic.")
        #        if not all(
        #            [
        #                n.degree(v) < 4 and n.in_degree(v) < 3 and n.out_degree(v) < 3
        #                for v in n.nodes
        #            ]
        #        ):
        #            raise serializers.ValidationError("The network is not binary.")
        return edges

    def save(self):
        n = Network()
        n.add_edges_from(self.validated_data.get("edges", []))
        self.validated_data["nodes"] = self.validated_data.get("nodes", [])
        node_set = set(self.validated_data["nodes"])
        self.validated_data["nodes"] += list(set(n.nodes).difference(node_set))
        self.validated_data["binary"] = n.is_binary()
        self.validated_data["classes"] = [
            c.value
            for c in NetworkClass
            if n.check_class(c) and c != NetworkClass.BI
        ]

        self.validated_data["number_of_roots"] = len(n.roots)
        self.validated_data["number_of_leaves"] = len(n.leaves)
        self.validated_data["reticulation_number"] = n.reticulation_number
        self.validated_data["node_positions"] = self.validated_data.get(
            "node_positions", n.calculate_node_positions()
        )
        super().save()

    class Meta:
        model = NetworkModel
        fields = ("id", "url", "nodes", "edges", "labels", "node_positions")
        extra_kwargs = {
            "url": {
                "lookup_field": "pk",
                "view_name": "api:network-detail",
            },
        }


class NetworkViewSerializer(NetworkSerializer):
    class Meta(NetworkSerializer.Meta):
        fields = "__all__"
