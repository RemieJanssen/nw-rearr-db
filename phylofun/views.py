from phylofun.models import Network
from phylofun.serializers import NetworkSerializer
from phylofun.models import Solution
from phylofun.serializers import SolutionSerializer
from phylofun.models import RearrangementProblem
from phylofun.serializers import RearrangementProblemSerializer
from rest_framework.viewsets import ModelViewSet

class SolutionViewSet(ModelViewSet):
    model = Solution
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()

class NetworkViewSet(ModelViewSet):
    model = Network
    serializer_class = NetworkSerializer
    queryset = Network.objects.all()

class RearrangementProblemViewSet(ModelViewSet):
    model = RearrangementProblem
    serializer_class = RearrangementProblemSerializer
    queryset = RearrangementProblem.objects.all()
