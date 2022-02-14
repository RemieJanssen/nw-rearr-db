from django.db import models

from phylofun.network_tools.base import Network


class NetworkModel(models.Model):
    nodes = models.JSONField()
    edges = models.JSONField()
    labels = models.JSONField()

    @property
    def network(self):
        network = Network(nodes=self.nodes, labels=self.labels)
        network.add_edges_from(self.edges)
        return network
