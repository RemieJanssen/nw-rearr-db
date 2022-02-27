import pytest
from django.test import TestCase

from phylofun.network_tools import Network


@pytest.mark.network_tools
class TreeChildTestCase(TestCase):
    def test_binary_tree(self):
        edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5), (2, 6), (2, 7)]
        network = Network(edges=edges)
        assert network.is_tree_child()

    def test_non_binary_tree(self):
        edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5), (3, 6), (2, 7)]
        network = Network(edges=edges)
        assert network.is_tree_child()

    def test_stack(self):
        edges = [(0, 2), (1, 2), (2, 4), (3, 4)]
        network = Network(edges=edges)
        assert not network.is_tree_child()

        edges = [
            (0, 1),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 4),
            (3, 5),
            (4, 5),
            (4, 6),
            (5, 7),
        ]
        network = Network(edges=edges)
        assert not network.is_tree_child()

    def test_w_shape(self):
        edges = [(0, 3), (0, 4), (1, 4), (1, 5), (2, 5), (2, 6)]
        network = Network(edges=edges)

        edges = [
            (0, 1),
            (1, 2),
            (1, 3),
            (2, 4),
            (3, 5),
            (2, 6),
            (6, 7),
            (3, 7),
            (6, 9),
            (4, 8),
            (4, 9),
            (9, 10),
            (7, 11),
        ]
        network = Network(edges=edges)
        assert not network.is_tree_child()

    def test_w_shape_non_binary(self):
        edges = [
            (0, 1),
            (1, 2),
            (1, 3),
            (2, 4),
            (3, 5),
            (2, 6),
            (6, 7),
            (3, 7),
            (6, 9),
            (4, 8),
            (4, 9),
            (9, 10),
            (7, 11),
            (1, 7),
            (6, 8),
            (8, 12),
        ]
        network = Network(edges=edges)
        assert not network.is_tree_child()


@pytest.mark.network_tools
class BinaryTestCase(TestCase):
    def test_tree(self):
        edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5), (2, 6), (2, 7)]
        network = Network(edges=edges)
        assert network.is_binary()

        edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5), (3, 6), (2, 7)]
        network = Network(edges=edges)
        assert not network.is_binary()

    def test_network(self):
        edges = [(0, 1), (1, 2), (1, 3), (2, 3), (2, 4), (3, 5)]
        network = Network(edges=edges)
        assert network.is_binary()

        edges = [(0, 1), (1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (1, 7)]
        network = Network(edges=edges)
        assert not network.is_binary()

        edges = [
            (0, 1),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 4),
            (3, 5),
            (4, 3),
            (4, 6),
        ]
        network = Network(edges=edges)
        assert not network.is_binary()

    def test_multi_rooted_network(self):
        edges = [(0, 1), (2, 1), (1, 3), (4, 3), (3, 5)]
        network = Network(edges=edges)
        assert network.is_binary()

        edges = [(0, 1), (1, 2), (1, 3), (4, 5), (5, 6), (5, 7)]
        network = Network(edges=edges)
        assert network.is_binary()
