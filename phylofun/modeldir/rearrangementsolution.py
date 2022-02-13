from django.db import models
from .rearrangementproblem import RearrangementProblemModel


class RearrangementSolutionModel(models.Model):
    """
    A solution to a problem is a sequence of rearrangement moves
    which turns network1 into network2.
    The resulting isomorphism must be provided as well.
    """

    problem = models.ForeignKey(
        RearrangementProblemModel,
        related_name="solutions",
        on_delete=models.CASCADE,
    )
    sequence = models.TextField()
    isomorphism = models.TextField()
