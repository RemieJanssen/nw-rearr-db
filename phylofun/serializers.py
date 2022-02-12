import ast

from phylofun.models import (
    NetworkModel,
    RearrangementProblemModel,
    SolutionModel,
)
from phylofun.network_tools.base import Network
from rest_framework import serializers
import networkx as nx


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

    def save(self):
        n = Network()
        n.add_edges_from(self.validated_data["edges"])
        print("remie")
        print(self.validated_data["nodes"])
        node_set = set(self.validated_data["nodes"])
        self.validated_data["nodes"] = list(node_set.union(set(n.nodes)))
        super().save()

    class Meta:
        model = NetworkModel
        fields = "__all__"


class RearrangementProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RearrangementProblemModel
        fields = "__all__"


class RearrangementProblemViewSerializer(serializers.ModelSerializer):
    network1 = NetworkSerializer()
    network2 = NetworkSerializer()

    class Meta:
        model = RearrangementProblemModel
        fields = "__all__"


class SolutionSerializer(serializers.ModelSerializer):

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
        #check whether the isomorphism covers all nodes of both networks
        isomorphism = data.get("isomorphism", None)
        if isomorphism:
            isomorphism_list = ast.literal_eval(isomorphism)
            nodes_nw_1 = [x[0] for x in isomorphism_list]
            nodes_nw_1_set = set(nodes_nw_1)
            nodes_nw_2 = [x[1] for x in isomorphism_list]
            nodes_nw_2_set = set(nodes_nw_2)
            if not (len(nodes_nw_1)==len(nodes_nw_1_set) and len(nodes_nw_2)==len(nodes_nw_2_set)):
                raise serializers.ValidationError(
                    "Each node can be mapped only once."
                )            
            if not set(nodes_nw_1)==set(data["problem"].network1.nodes):
                raise serializers.ValidationError(
                    "Isomorphism nodes should cover all nodes of network 1."
                )
            if not set(nodes_nw_2)==set(data["problem"].network2.nodes):
                raise serializers.ValidationError(
                    "Isomorphism nodes should cover all nodes of network 2."
                )
                
        #check whether the sequence solves the problem
        solution_valid = data["problem"].check_solution(data["sequence"],isomorphism=isomorphism)
        if not solution_valid:
            
            raise serializers.ValidationError(
                f"Sequence {'with isomorphism ' if isomorphism else ''} is not a valid solution for this problem."
            )
        return data
        
    class Meta:
        model = SolutionModel
        fields = "__all__"
    
        
