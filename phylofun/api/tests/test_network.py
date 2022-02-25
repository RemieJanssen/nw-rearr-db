from pytest import mark
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from phylofun import models
from phylofun.tests import factories


@mark.api
class NetworkTestCase(APITestCase):
    model = models.NetworkModel

    def setUp(self):
        self.obj = factories.NetworkFactory()
        self.list_url = reverse("api:network-list")
        self.detail_url = reverse("api:network-detail", (self.obj.id,))

    def create_filter_dataset(self):
        self.nw1 = factories.NetworkFactory(edges=[[0, 1]])
        self.nw2 = factories.NetworkFactory(nodes=[0, 1, 2])
        self.nw3 = factories.NetworkFactory()

    def test_create_minimal(self):
        result = self.client.post(self.list_url, {}, format="json")
        assert result.status_code == status.HTTP_201_CREATED

    def test_create_all(self):
        body = {
            "nodes": [6],
            "edges": [[1, 2]],
            "labels": [[2, 6]],
        }
        result = self.client.post(
            self.list_url,
            body,
            format="json",
        )
        assert result.status_code == status.HTTP_201_CREATED
        assert set(result.data["nodes"]) == set([1, 2, 6])

    def test_create_cyclic(self):
        body = {
            "edges": [[1, 2], [2, 3], [3, 1]],
        }
        result = self.client.post(
            self.list_url,
            body,
            format="json",
        )
        assert result.status_code == status.HTTP_400_BAD_REQUEST
        assert "edges" in result.data

    def test_update(self):
        body = {}
        result = self.client.patch(self.detail_url, body)
        assert result.status_code == status.HTTP_200_OK

    def test_destroy(self):
        result = self.client.delete(self.detail_url)
        assert result.status_code == status.HTTP_204_NO_CONTENT

    def test_uuid_filter(self):
        self.create_filter_dataset()
        result = self.client.get(self.list_url, {"id": self.obj.id})
        assert result.data["count"] == 1
