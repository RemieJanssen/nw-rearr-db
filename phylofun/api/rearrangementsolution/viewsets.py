from phylofun.models import RearrangementSolutionModel
from .serializers import RearrangementSolutionSerializer
from rest_framework.viewsets import ModelViewSet


class RearrangementSolutionViewSet(ModelViewSet):
    model = RearrangementSolutionModel
    serializer_class = RearrangementSolutionSerializer
    queryset = RearrangementSolutionModel.objects.all()
