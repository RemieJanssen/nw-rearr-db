import pytest
from django.test import TestCase

from phylofun.network_tools import CannotComputeError, Network


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
        edges = [
            (0, 3),
            (0, 4),
            (1, 4),
            (1, 5),
            (2, 5),
            (2, 6),
            (4, 7),
            (5, 8),
        ]
        network = Network(edges=edges)
        assert not network.is_tree_child()

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
class StackFreeTestCase(TestCase):
    def test_binary_tree(self):
        edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5), (2, 6), (2, 7)]
        network = Network(edges=edges)
        assert network.is_stack_free()

    def test_non_binary_tree(self):
        edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5), (3, 6), (2, 7)]
        network = Network(edges=edges)
        assert network.is_stack_free()

    def test_stack(self):
        edges = [(0, 2), (1, 2), (2, 4), (3, 4)]
        network = Network(edges=edges)
        assert not network.is_stack_free()

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
        assert not network.is_stack_free()

    def test_w_shape(self):
        edges = [(0, 3), (0, 4), (1, 4), (1, 5), (2, 5), (2, 6)]
        network = Network(edges=edges)
        assert network.is_stack_free()

        edges = [
            (0, 1),
            (1, 2),
            (1, 3),
            (2, 4),
            (2, 6),
            (3, 5),
            (3, 7),
            (4, 8),
            (4, 9),
            (6, 7),
            (6, 9),
            (7, 10),
            (9, 11),
        ]
        network = Network(edges=edges)
        assert network.is_stack_free()

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
        assert network.is_stack_free()


@pytest.mark.network_tools
class BinaryTestCase(TestCase):
    def test_tree(self):
        edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5), (2, 6), (2, 7)]
        network = Network(edges=edges)
        assert network.is_binary()

    def test_non_binary_tree(self):
        edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5), (3, 6), (2, 7)]
        network = Network(edges=edges)
        assert not network.is_binary()

    def test_network(self):
        edges = [(0, 1), (1, 2), (1, 3), (2, 3), (2, 4), (3, 5)]
        network = Network(edges=edges)
        assert network.is_binary()

    def test_network_non_binary_tree_node(self):
        edges = [(0, 1), (1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (1, 7)]
        network = Network(edges=edges)
        assert not network.is_binary()

    def test_network_non_binary_reticulation(self):
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

    def test_disjoint_trees(self):
        edges = [(0, 1), (1, 2), (1, 3), (4, 5), (5, 6), (5, 7)]
        network = Network(edges=edges)
        assert network.is_binary()


class TreeBasedTestCase(TestCase):
    def test_tree(self):
        edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5), (2, 6), (2, 7)]
        network = Network(edges=edges)
        assert network.is_tree_based()

    def test_non_binary_tree(self):
        edges = [
            (0, 1),
            (1, 2),
            (1, 3),
            (3, 4),
            (3, 5),
            (3, 6),
            (2, 7),
            (2, 8),
        ]
        network = Network(edges=edges)
        with pytest.raises(
            CannotComputeError,
            match="tree-basedness cannot be computed for non-binary networks yet.",
        ):
            network.is_tree_based()

    def test_tree_based_network(self):
        edges = [
            (0, 1),
            (1, 2),
            (1, 3),
            (2, 4),
            (3, 4),
            (2, 5),
            (3, 6),
            (4, 7),
        ]
        network = Network(edges=edges)
        assert network.is_tree_based()

    def test_tree_based_network_N_fence(self):
        # diamond shape network
        edges = [(0, 1), (1, 2), (1, 3), (2, 4), (2, 3), (3, 4), (4, 5)]
        network = Network(edges=edges)
        assert network.is_tree_based()

    def test_non_tree_based_network(self):
        edges = [
            (0, 1),
            (1, 2),
            (1, 3),
            (2, 4),
            (2, 5),
            (3, 6),
            (3, 7),
            (4, 6),
            (4, 5),
            (7, 8),
            (5, 8),
            (6, 9),
            (7, 9),
            (8, 10),
            (9, 11),
        ]
        network = Network(edges=edges)
        assert not network.is_tree_based()

    def test_disjoint_trees(self):
        edges = [(0, 1), (1, 2), (1, 3), (4, 5), (5, 6), (5, 7)]
        network = Network(edges=edges)
        assert not network.is_tree_based()

    def test_multi_rooted_network(self):
        edges = [(0, 1), (2, 1), (1, 3), (4, 3), (3, 5)]
        network = Network(edges=edges)
        assert not network.is_tree_based()


class OrchardTestCase(TestCase):
    def test_add_leaf_edge(self):
        edges = [(-1, -2), (-1, -3)]
        network = Network(edges=edges)
        assert network.is_orchard()

    def test_tree(self):
        edges = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5), (2, 6), (2, 7)]
        network = Network(edges=edges)
        assert network.is_orchard()

    def test_non_binary_tree(self):
        edges = [
            (0, 1),
            (1, 2),
            (1, 3),
            (3, 4),
            (3, 5),
            (2, 6),
            (2, 7),
            (2, 8),
        ]
        network = Network(edges=edges)
        assert network.is_orchard()

    def test_orchard_network(self):
        edges = [
            (0, 1),
            (1, 2),
            (1, 3),
            (2, 4),
            (3, 4),
            (2, 5),
            (3, 6),
            (4, 7),
        ]
        network = Network(edges=edges)
        assert network.is_orchard()

    def test_non_orchard_network(self):
        edges = [
            (3, 4),
            (4, 6),
            (4, 5),
            (5, 7),
            (5, 8),
            (6, 7),
            (6, 8),
            (7, 9),
            (8, 10),
        ]
        network = Network(edges=edges)
        assert not network.is_orchard()
