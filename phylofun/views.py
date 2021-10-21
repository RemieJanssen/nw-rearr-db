from phylofun.models import (
    NetworkModel,
    RearrangementProblemModel,
    SolutionModel,
)
from phylofun.serializers import (
    NetworkSerializer,
    RearrangementProblemSerializer,
    SolutionSerializer,
)
from rest_framework.viewsets import ModelViewSet


class SolutionViewSet(ModelViewSet):
    model = SolutionModel
    serializer_class = SolutionSerializer
    queryset = SolutionModel.objects.all()


class NetworkViewSet(ModelViewSet):
    model = NetworkModel
    serializer_class = NetworkSerializer
    queryset = NetworkModel.objects.all()


class RearrangementProblemViewSet(ModelViewSet):
    model = RearrangementProblemModel
    serializer_class = RearrangementProblemSerializer
    queryset = RearrangementProblemModel.objects.all()
