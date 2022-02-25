import pytest
from django.test import TestCase

from phylofun.network_tools import InvalidMoveDefinition, Move, MoveType


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

    def test_invalid_move_target_equals_moving_edge(self):
        with pytest.raises(
            InvalidMoveDefinition,
            match="Moving edge must not be the target edge.",
        ):
            Move(
                origin=(0, 1),
                moving_edge=(2, 3),
                target=(2, 3),
                move_type=MoveType.TAIL,
            )

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

    def test_make_move_none(self):
        m = Move(
            move_type=MoveType.NONE,
        )
        assert m.move_type == MoveType.NONE
