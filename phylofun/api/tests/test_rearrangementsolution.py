from pytest import mark
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from phylofun import models
from phylofun.tests import factories


@mark.api
class RearrangementSolutionTestCase(APITestCase):
    model = models.RearrangementSolutionModel

    def setUp(self):
        self.nw1 = factories.NetworkFactory(nodes=[1, 2], labels=[[1, 1]])
        self.nw2 = factories.NetworkFactory(nodes=[2, 3], labels=[[2, 1]])
        self.problem = factories.RearrangementProblemFactory(
            network1=self.nw1,
            network2=self.nw2,
        )
        self.obj = factories.RearrangementSolutionFactory(
            problem=self.problem,
            sequence=[],
            isomorphism=[],
        )
        self.list_url = reverse("api:rearrangementsolution-list")
        self.detail_url = reverse(
            "api:rearrangementsolution-detail", (self.obj.id,)
        )

    def create_filter_dataset(self):
        self.sol1 = factories.RearrangementSolutionFactory(
            problem=self.problem
        )
        self.sol2 = factories.RearrangementSolutionFactory(
            problem=self.problem
        )
        self.sol3 = factories.RearrangementSolutionFactory(
            problem=self.problem
        )

    def test_create(self):
        body = {
            "problem": reverse(
                "api:rearrangementproblem-detail", (self.problem.id,)
            ),
            "sequence": [
                {
                    "move_type": "NONE",
                },
            ],
            "isomorphism": [[1, 2], [2, 3]],
        }
        result = self.client.post(
            self.list_url,
            body,
            format="json",
        )
        assert result.status_code == status.HTTP_201_CREATED

    def test_create_missing_move_type(self):
        body = {
            "problem": reverse(
                "api:rearrangementproblem-detail", (self.problem.id,)
            ),
            "sequence": [
                {
                    "origin": [0, 1],
                    "target": [2, 3],
                    "moving_edge": [4, 5],
                },
            ],
            "isomorphism": [[1, 2], [2, 3]],
        }
        result = self.client.post(
            self.list_url,
            body,
            format="json",
        )
        assert result.status_code == status.HTTP_400_BAD_REQUEST
        assert result.data["sequence"][0][0] == "A move_type is mandatory."

    def test_create_invalid_none_type_move(self):
        body = {
            "problem": reverse(
                "api:rearrangementproblem-detail", (self.problem.id,)
            ),
            "sequence": [
                {
                    "move_type": "NONE",
                    "moving_edge": [4, 5],
                },
            ],
            "isomorphism": [[1, 2], [2, 3]],
        }
        result = self.client.post(
            self.list_url,
            body,
            format="json",
        )
        assert result.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            result.data["sequence"][0][0]
            == "move_type NONE does not take additional data."
        )

    def test_create_invalid_tail_rspr_move(self):
        body = {
            "problem": reverse(
                "api:rearrangementproblem-detail", (self.problem.id,)
            ),
            "sequence": [
                {
                    "move_type": "TAIL",
                    "moving_edge": [4, 5],
                },
            ],
            "isomorphism": [],
        }
        result = self.client.post(
            self.list_url,
            body,
            format="json",
        )
        assert result.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            result.data["sequence"][0][0]
            == "One of origin, moving_edge, or target is missing in a TAIL move"
        )

    def test_create_invalid_move_type(self):
        body = {
            "problem": reverse(
                "api:rearrangementproblem-detail", (self.problem.id,)
            ),
            "sequence": [
                {
                    "move_type": "NONX",
                },
            ],
            "isomorphism": [],
        }
        result = self.client.post(
            self.list_url,
            body,
            format="json",
        )
        assert result.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            result.data["sequence"][0][0] == "move_type NONX is not supported."
        )

    def test_create_invalid_solution(self):
        body = {
            "problem": reverse(
                "api:rearrangementproblem-detail", (self.problem.id,)
            ),
            "sequence": [
                {
                    "move_type": "NONE",
                },
                {
                    "move_type": "TAIL",
                    "origin": [0, 1],
                    "target": [2, 3],
                    "moving_edge": [4, 5],
                },
            ],
            "isomorphism": [[1, 2], [2, 3]],
        }
        result = self.client.post(
            self.list_url,
            body,
            format="json",
        )
        assert result.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            result.data["non_field_errors"][0]
            == "Sequence with isomorphism is not a valid solution for this problem."
        )

    def test_create_missing_isomorphism(self):
        body = {
            "problem": reverse(
                "api:rearrangementproblem-detail", (self.problem.id,)
            ),
            "sequence": [],
            "isomorphism": [],
        }
        result = self.client.post(
            self.list_url,
            body,
            format="json",
        )
        assert result.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            result.data["non_field_errors"][0]
            == "Must provide an isomorphism for non-trivial networks"
        )

    def test_create_invalid_isomorphism_missing_nodes_nw1(self):
        body = {
            "problem": reverse(
                "api:rearrangementproblem-detail", (self.problem.id,)
            ),
            "sequence": [],
            "isomorphism": [[1, 1]],
        }
        result = self.client.post(
            self.list_url,
            body,
            format="json",
        )
        assert result.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            result.data["non_field_errors"][0]
            == "Isomorphism nodes should cover all nodes of network 1."
        )

    def test_create_invalid_isomorphism_missing_nodes_nw2(self):
        body = {
            "problem": reverse(
                "api:rearrangementproblem-detail", (self.problem.id,)
            ),
            "sequence": [],
            "isomorphism": [[1, 1], [2, 3]],
        }
        result = self.client.post(
            self.list_url,
            body,
            format="json",
        )
        assert result.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            result.data["non_field_errors"][0]
            == "Isomorphism nodes should cover all nodes of network 2."
        )

    def test_create_invalid_isomorphism_double_mapping(self):
        body = {
            "problem": reverse(
                "api:rearrangementproblem-detail", (self.problem.id,)
            ),
            "sequence": [],
            "isomorphism": [[1, 2], [1, 3], [2, 3]],
        }
        result = self.client.post(
            self.list_url,
            body,
            format="json",
        )
        assert result.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            result.data["non_field_errors"][0]
            == "Each node may be mapped only once."
        )

    def test_update(self):
        body = {
            "problem": reverse(
                "api:rearrangementproblem-detail", (self.problem.id,)
            ),
            "sequence": [{"move_type": "NONE"}],
            "isomorphism": [[1, 2], [2, 3]],
        }
        result = self.client.patch(self.detail_url, body, format="json")
        print(result.data)
        assert result.status_code == status.HTTP_200_OK

    def test_destroy(self):
        result = self.client.delete(self.detail_url)
        assert result.status_code == status.HTTP_204_NO_CONTENT

    def test_uuid_filter(self):
        self.create_filter_dataset()
        result = self.client.get(self.list_url, {"id": self.obj.id})
        assert result.data["count"] == 1
