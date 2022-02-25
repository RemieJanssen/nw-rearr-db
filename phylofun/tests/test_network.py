from unittest import mock

import pytest
from django.test import TestCase

from phylofun.network_tools import Move, MoveType, Network


@pytest.mark.network_tools
class NetworkTestCase(TestCase):
    def test_empty_network(self):
        network = Network()
        assert list(network.nodes) == []

    def test_nodes_only_network(self):
        nodes = [0, 1, 2]
        network = Network(nodes=nodes)
        assert set(network.nodes) == set(nodes)

    def test_edges_only(self):
        edges = [(0, 1), (1, 2)]
        network = Network(edges=edges)
        assert set(network.edges) == set(edges)
        assert set(network.nodes) == set([0, 1, 2])

    def test_nodes_and_edges(self):
        nodes = [0, 1, 10]
        edges = [(0, 1), (1, 2)]
        network = Network(edges=edges, nodes=nodes)
        assert set(network.edges) == set(edges)
        assert set(network.nodes) == set([0, 1, 2, 10])

    def test_all(self):
        nodes = [0, 1, 10]
        edges = [(0, 1), (1, 2)]
        labels = [(2, 1), (10, 2)]
        network = Network(edges=edges, nodes=nodes, labels=labels)
        assert set(network.edges) == set(edges)
        assert set(network.nodes) == set([0, 1, 2, 10])
        assert network.nodes[10]["label"] == 2

    def test_apply_tail_move_changes(self):
        edges = [(0, 1), (1, 5), (1, 2), (2, 3), (2, 4)]
        network = Network(edges=edges)
        move = Move(
            origin=(1, 4),
            moving_edge=(2, 3),
            target=(1, 5),
            move_type=MoveType.TAIL,
        )
        network.apply_move(move)
        assert network.edges == set([(0, 1), (1, 2), (2, 5), (1, 4), (2, 3)])

    def test_apply_tail_move_no_changes(self):
        edges = [(0, 1), (1, 5), (1, 2), (2, 3), (2, 4)]
        network = Network(edges=edges)
        move = Move(
            origin=(1, 4),
            moving_edge=(2, 3),
            target=(2, 5),
            move_type=MoveType.TAIL,
        )
        network.apply_move(move)
        assert network.edges == set(edges)

    def test_apply_move_sequence(self):
        edges = [(0, 1), (1, 5), (1, 2), (2, 3), (2, 4)]
        network = Network(edges=edges)
        move = Move(
            move_type=MoveType.NONE,
        )
        network.apply_move_sequence([move])
        assert network.edges == set(edges)

    def test_child(self):
        edges = [(0, 1), (1, 2), (1, 3)]
        network = Network(edges=edges)
        assert network.child(0) == 1
        assert network.child(1, exclude=[2, 5]) == 3
        with mock.patch("random.getrandbits", return_value=1):
            assert network.child(1, randomNodes=True) == 3

    def test_parent(self):
        edges = [(0, 1), (2, 1), (1, 3)]
        network = Network(edges=edges)
        assert network.parent(3) == 1
        assert network.parent(1, exclude=[2, 5]) == 0
        with mock.patch("random.getrandbits", return_value=1):
            assert network.parent(1, randomNodes=True) == 2
