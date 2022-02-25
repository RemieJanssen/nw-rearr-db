import networkx as nx
from rest_framework import serializers

from phylofun.models import NetworkModel
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
