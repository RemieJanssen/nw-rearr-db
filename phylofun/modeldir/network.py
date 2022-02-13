from django.db import models


class NetworkModel(models.Model):
    nodes = models.TextField()
    edges = models.TextField()
    labels = models.TextField()
