from phylofun.models import (
    NetworkModel,
    RearrangementProblemModel,
    SolutionModel,
)
from phylofun.serializers import (
    NetworkSerializer,
    RearrangementProblemSerializer,
    RearrangementProblemViewSerializer,
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
    queryset = RearrangementProblemModel.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return RearrangementProblemSerializer
        return RearrangementProblemViewSerializer
