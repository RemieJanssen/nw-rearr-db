from rest_framework.viewsets import ModelViewSet

from phylofun.models import NetworkModel

from .filters import NetworkFilterSet
from .serializers import NetworkSerializer, NetworkViewSerializer


class NetworkViewSet(ModelViewSet):
    model = NetworkModel
    serializer_class = NetworkSerializer
    filterset_class = NetworkFilterSet
    queryset = NetworkModel.objects.all()

    def get_serializer_class(self):
        if self.action in ["post", "create", "update", "partial_update"]:
            return NetworkSerializer
        return NetworkViewSerializer
