from copy import deepcopy

from .network import is_isomorphic


class RearrangementProblem(object):
    def __init__(self, network1, network2, move_type):
        self.network1 = network1
        self.network2 = network2
        self.move_type = move_type

    def check_solution(self, seq_moves, isomorphism=None):
        if not all([move.is_type(self.move_type) for move in seq_moves]):
            return False

        network1_copy = deepcopy(self.network1)
        network1_copy.apply_move_sequence(seq_moves)

        return is_isomorphic(
            network1_copy, self.network2, partial_isomorphism=isomorphism
        )
