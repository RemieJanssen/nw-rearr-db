import factory

from phylofun import models


class NetworkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.NetworkModel


class RearrangementProblemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RearrangementProblemModel

    network1 = factory.SubFactory(NetworkFactory)
    network2 = factory.SubFactory(NetworkFactory)
