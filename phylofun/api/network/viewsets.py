from rest_framework.viewsets import ModelViewSet

from phylofun.models import NetworkModel

from .filters import NetworkFilterSet
from .serializers import NetworkSerializer


class NetworkViewSet(ModelViewSet):
    model = NetworkModel
    serializer_class = NetworkSerializer
    filterset_class = NetworkFilterSet
    queryset = NetworkModel.objects.all()
