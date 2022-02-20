import pytest
from django.test import TestCase

from phylofun.network_tools.base import (
    InvalidMove,
    InvalidMoveDefinition,
    Move,
    MoveType,
    Network,
    RearrangementProblem,
)


@pytest.mark.network_tools
class MoveTestCase(TestCase):
    def test_invalid_move_rspr(self):
        with pytest.raises(
            InvalidMoveDefinition,
            match="rSPR moves must be defined as moves of type tail or head.",
        ):
            Move(
                origin=(0, 1),
                moving_edge=(2, 3),
                target=(4, 5),
                move_type=MoveType.RSPR,
            )

    def test_invalid_move_missing_move_type(self):
        with pytest.raises(InvalidMoveDefinition, match="Missing move_type."):
            Move(origin=(0, 1), moving_edge=(2, 3), target=(4, 5))

    def test_invalid_move_missing_arg(self):
        with pytest.raises(
            InvalidMoveDefinition,
            match="Missing one of origin, moving_edge, or target.",
        ):
            Move(origin=(0, 1), moving_edge=(2, 3), move_type=MoveType.TAIL)

    def test_make_move_head(self):
        m = Move(
            origin=(0, 1),
            moving_edge=(2, 3),
            target=(4, 5),
            move_type=MoveType.HEAD,
        )
        assert m.move_type == MoveType.HEAD

    def test_make_move_tail(self):
        m = Move(
            origin=(0, 1),
            moving_edge=(2, 3),
            target=(4, 5),
            move_type=MoveType.TAIL,
        )
        assert m.move_type == MoveType.TAIL


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


@pytest.mark.network_tools
class RearrangementTestCase(TestCase):
    @staticmethod
    def setup_simple_problem():
        nw_1 = Network(
            nodes=[10],
            edges=[[0, 1], [1, 2], [1, 3], [2, 3], [2, 4], [3, 5]],
            labels=[[4, 1], [5, 2]],
        )
        nw_2 = Network(
            nodes=[10],
            edges=[[0, 1], [1, 2], [1, 3], [3, 2], [2, 4], [3, 5]],
            labels=[[4, 1], [5, 2]],
        )
        move_type = MoveType.RSPR
        return RearrangementProblem(nw_1, nw_2, move_type)

    def test_simple_problem(self):
        self.setup_simple_problem()
        assert True

    def test_apply_valid_move(self):
        m = Move(
            origin=(2, 5),
            moving_edge=(1, 3),
            target=(2, 4),
            move_type=MoveType.HEAD,
        )
        problem = self.setup_simple_problem()
        problem.network1.apply_move(m)
        assert True

    def test_apply_invalid_move_cycle(self):
        m = Move(
            origin=(2, 5),
            moving_edge=(1, 3),
            target=(0, 1),
            move_type=MoveType.HEAD,
        )
        problem = self.setup_simple_problem()
        with pytest.raises(InvalidMove, match="the move would create a cycle"):
            problem.network1.apply_move(m)

    def test_apply_invalid_move_not_movable(self):
        m = Move(
            origin=(1, 3),
            moving_edge=(2, 4),
            target=(3, 5),
            move_type=MoveType.TAIL,
        )
        problem = self.setup_simple_problem()
        with pytest.raises(InvalidMove, match="the edge is not movable"):
            problem.network1.apply_move(m)
