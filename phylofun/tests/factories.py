import factory

from phylofun import models


class NetworkFactory(factory.django.DjangoModelFactory):
    number_of_roots = 0
    number_of_leaves = 0
    reticulation_number = 0
    binary = True

    class Meta:
        model = models.NetworkModel


class RearrangementProblemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RearrangementProblemModel

    network1 = factory.SubFactory(NetworkFactory)
    network2 = factory.SubFactory(NetworkFactory)
    goal_length = 10


class RearrangementSolutionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RearrangementSolutionModel

    problem = factory.SubFactory(RearrangementProblemFactory)
    sequence = []
    isomorphism = []
