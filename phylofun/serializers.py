from rest_framework import serializers
from phylofun.models import Network
from phylofun.models import RearrangementProblem
from phylofun.models import Solution
import networkx as nx
import ast

class NetworkSerializer(serializers.ModelSerializer):
    def validate_nodes(self, nodes):
        try:
            nodes_list = list(ast.literal_eval(nodes))
            nodes_list_check_ints = [isinstance(x,int) for x in nodes_list]
            if all(nodes_list_check_ints):
                return nodes_list
            raise serializers.ValidationError("List of nodes contains non-int values.")
        except serializers.ValidationError as e:
            raise e("List of nodes is not in list format.")

    def validate_edges(self, edges):
        try: 
            edge_list = ast.literal_eval(edges)
            edge_list_check = [
                isinstance(edge, tuple) 
                and len(edge)==2 
                and all([isinstance(x,int) for x in edge])
                for edge in edge_list
            ]
            if all(edge_list_check):
                return edges
            raise serializers.ValidationError("List contains an invalid edge.")
        except ValueError as e:       
            raise serializers.ValidationError("Not a valid list of edges")

    def save(self):
        edges = self.validated_data['edges']
        nodes = set()
        for e in edges:
            nodes.update(e)
          

    class Meta:
        model = Network
        fields = '__all__'

class RearrangementProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RearrangementProblem
        fields = '__all__'

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = '__all__'

