import networkx as nx
import ast

class Network(nx.DiGraph):
    def apply_move(self, move):
        pass

    def apply_move_sequence(self, seq_moves):
        for move in seq_moves:
            self.apply_move(move)


class RearrangementProblem(object):
    def __init__(self, network1, network2, move_type)
        self.network1=network1
        self.network2=network2
        self.move_type=move_type

    def check_solution(self, seq_moves):
        
        network1_copy = copy(network1)
        network1_copy.apply_move_sequence(seq_moves)

class MoveType:
    NONE = 0
    TAIL = 1
    HEAD = 2
    RSPR = 3    


class Move(object):
    def __init__(self, move_tuple):
        self.origin     =move_tuple[0]
        self.moving_edge=move_tuple[1]
        self.target     =move_tuple[2]
        self.moving_node=move_tuple[3]
        if self.moving_node == self.moving_edge[0]:
            self.type=MoveType.TAIL
        else:
            self.type=MoveType.HEAD


class Solution(object):
    def __init__(self, moves_string)
        self.move_sequence = ast.literal_eval(moves_string)
        move_types_tails_boolean = [is_tail_move(move) for move in self.move_sequence]
        self.head_used = len(move_sequence)>0 and not all(move_types_tails_boolean)
        self.tail_used = len(move_sequence)>0 and any(move_types_tails_boolean)
