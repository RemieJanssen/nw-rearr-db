from django.db import models

from phylofun.network_tools import Network


class NetworkModel(models.Model):
    nodes = models.JSONField(default=[])
    edges = models.JSONField(default=[])
    labels = models.JSONField(default=[])

    @property
    def network(self):
        return Network(
            nodes=self.nodes,
            edges=self.edges,
            labels=self.labels,
        )
