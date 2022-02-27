from django.conf.urls import include
from django.urls import path, re_path

from phylofun.routers import OrderedDefaultRouter

from .network.viewsets import NetworkViewSet
from .rearrangementproblem.viewsets import RearrangementProblemViewSet
from .rearrangementsolution.viewsets import RearrangementSolutionViewSet

app_name = "phylofun"
router = OrderedDefaultRouter()

router.register(r"networks", NetworkViewSet, basename="network")
router.register(r"rearrangementsolutions", RearrangementSolutionViewSet, basename="rearrangementsolution")
router.register(r"rearrangementproblems", RearrangementProblemViewSet, basename="rearrangementproblem")

urlpatterns = (list(router.urls))

urlpatterns = [re_path(r"", include(urlpatterns))]
