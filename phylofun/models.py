from django.db import models


class Network(models.Model):
    nodes = models.TextField()
    edges = models.TextField()


class RearrangementProblem(models.Model):
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
        Network,
        related_name="problems1",
        on_delete=models.CASCADE,
    )
    network2 = models.ForeignKey(
        Network,
        related_name="problems2",
        on_delete=models.CASCADE,
    )
    partial_isomorphism = models.TextField()
    move_type = models.SmallIntegerField("move type", choices=MOVE_TYPES)
    vertical_allowed = models.BooleanField(default=False)


class Solution(models.Model):
    """
    A solution to a problem is a sequence of rearrangement moves 
    which turns network1 into network2.
    The resulting isomorphism must be provided as well.
    """
    problem = models.ForeignKey(
        RearrangementProblem,
        related_name="solutions",
        on_delete=models.CASCADE,
    )
    sequence = models.TextField()
    isomorphism = models.TextField()

