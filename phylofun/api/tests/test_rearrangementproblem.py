from pytest import mark
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from phylofun import models
from phylofun.network_tools import RearrangementProblem
from phylofun.tests import factories


@mark.api
class RearrangementProblemTestCase(APITestCase):
    model = models.RearrangementSolutionModel

    def setUp(self):
        self.nw1 = factories.NetworkFactory()
        self.nw2 = factories.NetworkFactory()
        self.obj = factories.RearrangementProblemFactory(
            network1=self.nw1,
            network2=self.nw2,
        )
        self.list_url = reverse("api:rearrangementproblem-list")
        self.detail_url = reverse(
            "api:rearrangementproblem-detail", (self.obj.id,)
        )

    def create_filter_dataset(self):
        self.pr1 = factories.RearrangementProblemFactory()
        self.pr2 = factories.RearrangementProblemFactory()
        self.pr3 = factories.RearrangementProblemFactory()

    def test_model_to_object(self):
        rearrangementproblem_object = self.obj.rearrangement_problem
        assert isinstance(rearrangementproblem_object, RearrangementProblem)

    def test_create_minimal(self):
        body = {
            "network1": reverse("api:network-detail", (self.nw1.id,)),
            "network2": reverse("api:network-detail", (self.nw2.id,)),
            "move_type": "tail moves",
            "goal_length": 5,
        }
        result = self.client.post(self.list_url, body, format="json")
        assert result.status_code == status.HTTP_201_CREATED

    def test_create_all(self):
        body = {
            "network1": reverse("api:network-detail", (self.nw1.id,)),
            "network2": reverse("api:network-detail", (self.nw2.id,)),
            "move_type": "head moves",
            "vertical_allowed": "False",
            "goal_length": 5,
        }
        result = self.client.post(self.list_url, body, format="json")
        assert result.status_code == status.HTTP_201_CREATED

    def test_update(self):
        body = {"vertical_allowed": True}
        result = self.client.patch(self.detail_url, body)
        assert result.status_code == status.HTTP_200_OK
        assert result.data["vertical_allowed"] is True

    def test_destroy(self):
        result = self.client.delete(self.detail_url)
        assert result.status_code == status.HTTP_204_NO_CONTENT

    def test_uuid_filter(self):
        self.create_filter_dataset()
        result = self.client.get(self.list_url, {"id": self.obj.id})
        assert result.data["count"] == 1
