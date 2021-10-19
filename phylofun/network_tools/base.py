import networkx as nx
import ast

class Network(nx.DiGraph):
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges 

    def apply_move(self, move):
        """
        Apply a move to the network.
        returns True if successful, and False otherwise.        
        """
        if self.check_valid(move):
            if move.type in [MoveType.TAIL, MoveType.HEAD]:
                if move.moving_node in move.target:
                    # move does not impact the network
                    return True
                self.remove_edges_from([
                    (move.origin[0], move.moving_node), 
                    (move.moving_node, move.origin[1]), 
                    move.target,
                ])
                self.add_edges_from([
                    (move.target[0], move.moving_node), 
                    (move.moving_node, move.target[1]), 
                    move.origin,
                ])
                return True
            else:
                #TODO implement vertical moves
                return False
        else:
            # return False for invalid moves
            return False

    def apply_move_sequence(self, seq_moves):
        for move in seq_moves:
            self.apply_move(move)

    def check_valid(self, move):
        pass

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
        try:
            # horizontal move
            self.moving_node = move_tuple[3]
            self.target      = move_tuple[2]
            self.moving_edge = move_tuple[1]
            self.origin      = move_tuple[0]            
            if self.moving_node == self.moving_edge[0]:
                self.type=MoveType.TAIL
            else:
                self.type=MoveType.HEAD
        except:
            # vertical move
            pass


class Solution(object):
    def __init__(self, moves_string)
        self.move_sequence = ast.literal_eval(moves_string)
        move_types_tails_boolean = [is_tail_move(move) for move in self.move_sequence]
        self.head_used = len(move_sequence)>0 and not all(move_types_tails_boolean)
        self.tail_used = len(move_sequence)>0 and any(move_types_tails_boolean)
