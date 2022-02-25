from django.db import models

from phylofun.network_tools import RearrangementProblem

from .move import MOVE_TYPES, MoveType
from .network import NetworkModel


class RearrangementProblemModel(models.Model):
    """
    A rearrangement problem consists of two networks and a type of move
    that may be used to turn one network into the other.
    """

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
    move_type = models.CharField(
        "move type", choices=MOVE_TYPES, default=MoveType.NONE, max_length=4
    )
    vertical_allowed = models.BooleanField(default=False)

    @property
    def rearrangement_problem(self):
        return RearrangementProblem(
            self.network1.network, self.network2.network, self.move_type
        )
