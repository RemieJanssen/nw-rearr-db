import pytest
from django.test import TestCase

from phylofun.network_tools import (
    InvalidMove,
    Move,
    MoveType,
    Network,
    RearrangementProblem,
)


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

    def test_apply_invalid_head_move_cycle(self):
        m = Move(
            origin=(2, 5),
            moving_edge=(1, 3),
            target=(0, 1),
            move_type=MoveType.HEAD,
        )
        problem = self.setup_simple_problem()
        with pytest.raises(
            InvalidMove, match="reattachment would create a cycle"
        ):
            problem.network1.apply_move(m)

    def test_apply_invalid_tail_move_cycle(self):
        m = Move(
            origin=(0, 2),
            moving_edge=(1, 3),
            target=(3, 5),
            move_type=MoveType.TAIL,
        )
        problem = self.setup_simple_problem()
        with pytest.raises(
            InvalidMove, match="reattachment would create a cycle"
        ):
            problem.network1.apply_move(m)

    def test_apply_invalid_tail_move_not_movable_triangle(self):
        m = Move(
            origin=(1, 3),
            moving_edge=(2, 4),
            target=(0, 1),
            move_type=MoveType.TAIL,
        )
        problem = self.setup_simple_problem()
        with pytest.raises(
            InvalidMove, match="removal creates parallel edges"
        ):
            problem.network1.apply_move(m)

    def test_apply_invalid_head_move_not_movable_triangle(self):
        network = Network(
            edges=[[0, 1], [2, 3], [1, 3], [1, 4], [3, 4], [4, 5]],
        )

        m = Move(
            origin=(1, 4),
            moving_edge=(2, 3),
            target=(4, 5),
            move_type=MoveType.HEAD,
        )
        with pytest.raises(
            InvalidMove, match="removal creates parallel edges"
        ):
            network.apply_move(m)

    def test_apply_invalid_bad_origin(self):
        network = Network(
            edges=[[0, 1], [1, 2], [1, 3], [3, 4]],
        )
        m = Move(
            origin=(3, 4),
            moving_edge=(1, 2),
            target=(0, 1),
            move_type=MoveType.TAIL,
        )
        with pytest.raises(
            InvalidMove,
            match="origin does not match parent and child or moving_endpoint",
        ):
            network.apply_move(m)

    def test_apply_invalid_tail_move_parallel(self):
        network = Network(
            edges=[[0, 1], [1, 2], [3, 4], [4, 5], [4, 1]],
        )

        m = Move(
            origin=(3, 5),
            moving_edge=(4, 1),
            target=(0, 1),
            move_type=MoveType.TAIL,
        )
        with pytest.raises(
            InvalidMove, match="reattachment creates parallel edges"
        ):
            network.apply_move(m)

    def test_apply_invalid_head_move_parallel(self):
        network = Network(
            edges=[[0, 1], [1, 2], [3, 4], [4, 5], [4, 1]],
        )

        m = Move(
            origin=(0, 2),
            moving_edge=(4, 1),
            target=(4, 5),
            move_type=MoveType.HEAD,
        )
        with pytest.raises(
            InvalidMove, match="reattachment creates parallel edges"
        ):
            network.apply_move(m)
