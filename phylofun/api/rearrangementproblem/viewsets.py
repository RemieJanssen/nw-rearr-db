from rest_framework.viewsets import ModelViewSet

from phylofun.models import RearrangementProblemModel

from .filters import RearrangementProblemFilterSet
from .serializers import (
    RearrangementProblemSerializer,
    RearrangementProblemViewSerializer,
)


class RearrangementProblemViewSet(ModelViewSet):
    model = RearrangementProblemModel
    queryset = RearrangementProblemModel.objects.all()
    filterset_class = RearrangementProblemFilterSet

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return RearrangementProblemSerializer
        return RearrangementProblemViewSerializer
