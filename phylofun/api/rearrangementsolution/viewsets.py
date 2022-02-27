from rest_framework.viewsets import ModelViewSet

from phylofun.models import RearrangementSolutionModel

from .filters import RearrangementSolutionFilterSet
from .serializers import RearrangementSolutionSerializer


class RearrangementSolutionViewSet(ModelViewSet):
    model = RearrangementSolutionModel
    serializer_class = RearrangementSolutionSerializer
    filterset_class = RearrangementSolutionFilterSet
    queryset = RearrangementSolutionModel.objects.all()
