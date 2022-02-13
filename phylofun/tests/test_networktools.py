from django.test import TestCase
from pytest import mark

from phylofun.network_tools.base import (
    InvalidMoveDefinition,
    Move,
    MoveType,
    Network,
)


@mark.model
class NetworkTestCase(TestCase):
    def test_empty_network(self):
        network = Network()
        assert list(network.nodes) == []

    def test_nodes_only_network(self):
        network = Network()
        node_list = [0, 1, 2]
        network.add_nodes_from(node_list)
        assert list(network.nodes) == node_list


@mark.model
class MoveTestCase(TestCase):
    def test_invalid_move(self):
        try:
            Move(((0, 2), (3, 1), (4, 5)))
            assert False
        except InvalidMoveDefinition:
            assert True

    def test_make_move_head(self):
        m = Move(((0, 2), (3, 1), (4, 5), 1))
        assert m.type == MoveType.HEAD

    def test_make_move_tail(self):
        m = Move(((0, 2), (1, 3), (4, 5), 1))
        assert m.type == MoveType.TAIL
