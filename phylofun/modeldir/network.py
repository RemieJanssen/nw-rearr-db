from django.db import models

from phylofun.network_tools import Network, NetworkClass

NETWORK_CLASSES = [
    (x.value, x.value) for x in NetworkClass if x != NetworkClass.BI
]


class NetworkModel(models.Model):
    nodes = models.JSONField(default=list)
    edges = models.JSONField(default=list)
    labels = models.JSONField(default=list)

    number_of_roots = models.IntegerField()
    number_of_leaves = models.IntegerField()
    reticulation_number = models.IntegerField()

    binary = models.BooleanField()
    classes = models.CharField(max_length=100, choices=NETWORK_CLASSES)

    @property
    def network(self):
        return Network(
            nodes=self.nodes,
            edges=self.edges,
            labels=self.labels,
        )

    class Meta:
        ordering = [
            "binary",
            "number_of_roots",
            "number_of_leaves",
            "reticulation_number",
        ]
