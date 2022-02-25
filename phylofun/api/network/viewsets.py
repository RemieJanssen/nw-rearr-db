from phylofun.models import NetworkModel
from .serializers import NetworkSerializer
from rest_framework.viewsets import ModelViewSet


class NetworkViewSet(ModelViewSet):
    model = NetworkModel
    serializer_class = NetworkSerializer
    queryset = NetworkModel.objects.all()
