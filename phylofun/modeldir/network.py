from django.db import models

from phylofun.network_tools import Network


class NetworkModel(models.Model):
    nodes = models.JSONField()
    edges = models.JSONField()
    labels = models.JSONField()

    @property
    def network(self):
        return Network(
            nodes=self.nodes,
            edges=self.edges,
            labels=self.labels,
        )
