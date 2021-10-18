from rest_framework import serializers
from phylofun.models import Network
from phylofun.models import RearrangementProblem
from phylofun.models import Solution
import networkx as nx
import ast

class NetworkSerializer(serializers.ModelSerializer):
    def validate_nodes(self,nodes):
        try:
            nodes_list = list(ast.literal_eval(nodes))
            nodes_list_check_ints = [isinstance(x,int) for x in nodes_list]
            if all(nodes_list_check_ints):
                return nodes_list
            raise serializers.ValidationError("List of nodes contains non-int values.")
        except serializers.ValidationError as e:
            raise e("List of nodes is not in list format.")

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

