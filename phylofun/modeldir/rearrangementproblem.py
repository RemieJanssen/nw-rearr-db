from django.db import models
from .network import NetworkModel


class RearrangementProblemModel(models.Model):
    """
    A rearrangement problem consists of two networks and a type of move
    that may be used to turn one network into the other.
    """

    class MoveType:
        NONE = 0
        TAIL = 1
        HEAD = 2
        RSPR = 3

    MOVE_TYPES = (
        (MoveType.NONE, "no moves"),
        (MoveType.TAIL, "tail moves"),
        (MoveType.HEAD, "head moves"),
        (MoveType.RSPR, "rSPR moves"),
    )

    network1 = models.ForeignKey(
        NetworkModel,
        related_name="problems1",
        on_delete=models.CASCADE,
    )
    network2 = models.ForeignKey(
        NetworkModel,
        related_name="problems2",
        on_delete=models.CASCADE,
    )
    move_type = models.SmallIntegerField("move type", choices=MOVE_TYPES)
    vertical_allowed = models.BooleanField(default=False)
