from django.urls import path
from phylofun import views
from phylofun.routers import OrderedDefaultRouter
from django.conf.urls import include
from django.conf.urls import url

router = OrderedDefaultRouter()

router.register(r"networks", views.NetworkViewSet, basename="network")
router.register(r"solutions", views.SolutionViewSet, basename="solution")
router.register(r"rearrangementproblems", views.RearrangementProblemViewSet, basename="rearrangementproblem")

urlpatterns = (list(router.urls))

urlpatterns = [url(r"", include(urlpatterns))]
