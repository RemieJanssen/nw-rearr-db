from rest_framework import serializers
from phylofun.models import Network
from phylofun.models import RearrangementProblem
from phylofun.models import Solution


class NetworkSerializer(serializers.ModelSerializer):
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

