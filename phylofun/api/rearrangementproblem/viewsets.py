from phylofun.models import RearrangementProblemModel
from .serializers import (
    RearrangementProblemSerializer,
    RearrangementProblemViewSerializer,
)
from rest_framework.viewsets import ModelViewSet


class RearrangementProblemViewSet(ModelViewSet):
    model = RearrangementProblemModel
    queryset = RearrangementProblemModel.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return RearrangementProblemSerializer
        return RearrangementProblemViewSerializer
