import networkx as nx
import ast


class InvalidMoveError(Exception):
    pass


class Network(nx.DiGraph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "labels" in kwargs:
            for label in kwargs["labels"]:
                self.nodes[label[0]].label = label[1]

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
                self.remove_edges_from(
                    [
                        (move.origin[0], move.moving_node),
                        (move.moving_node, move.origin[1]),
                        move.target,
                    ]
                )
                self.add_edges_from(
                    [
                        (move.target[0], move.moving_node),
                        (move.moving_node, move.target[1]),
                        move.origin,
                    ]
                )
                return True
            else:
                # TODO implement vertical moves
                return False
        else:
            # return False for invalid moves
            return False

    def apply_move_sequence(self, seq_moves):
        for move in seq_moves:
            self.apply_move(move)

    def check_valid(self, move):
        """
        Checks whether a move is valid.

        :param move: an move of tyupe Move
        :return: True if the move is allowed, False otherwise.
        """

        if move.moving_edge == move.target:
            return False
        if not self.check_movable(move.moving_edge, moving_endpoint):
            return False
        if move.moving_node == move.moving_edge[0]:
            # tail move, check whether the move.target is below the head of the moving edge
            if nx.has_path(self, move.moving_edge[1], move.target[0]):
                # the move would create a cycle
                return False
            if move.target[1] == move.moving_edge[1]:
                # the move would create parallel edges
                return False
        elif move.moving_node == move.moving_edge[1]:
            # head move, check whether the move.target is above the tail of the moving edge
            if nx.has_path(self, move.target[1], move.moving_edge[0]):
                # the move would create a cycle
                return False
            if move.target[0] == move.moving_edge[0]:
                # the move would create parallel edges
                return False
        else:
            # The moving endpoint is not part of the moving edge
            # Checked in CheckMovable as well, redundant?!
            return False
        # No parallel edges at start location
        # No cycle
        # No parallel edges at end location
        # So the move is valid
        return True

    def check_movable(self, moving_edge, moving_endpoint):
        """
        Checks whether an endpoint of an edge is movable.

        :param moving_edge: an edge.
        :param moving_endpoint: a node, specifically, an endpoint of the moving_edge.
        :return: True if the endpoint of the edge is movable, False otherwise.
        """
        if moving_endpoint == moving_edge[0]:
            # Tail move
            if self.in_degree(moving_endpoint) in (0, 2):
                # cannot move the tail if it is a reticulation or root
                return False
        elif moving_endpoint == moving_edge[1]:
            # Head move
            if self.out_degree(moving_endpoint) in (0, 2):
                # cannot move the head if it is a tree node or leaf
                return False
        else:
            # Moving endpoint is not part of the moving edge
            return False
        # Now check for triangles, by finding the other parent and child of the moving endpoint
        parent_of_moving_endpoint = self.parent(
            moving_endpoint, exclude=[moving_edge[0]]
        )
        child_of_moving_endpoint = self.child(moving_endpoint, exclude=[moving_edge[1]])
        # if there is an edge from the parent to the child, there is a triangle
        # Otherwise, it is a movable edge
        return not self.has_edge(parent_of_moving_endpoint, child_of_moving_endpoint)

    def child(self, node, exclude=[], randomNodes=False):
        """
        Finds a child node of a node.

        :param node: a node of self.
        :param exclude: a set of nodes of self.
        :param randomNodes: a boolean value.
        :return: a child of node that is not in the set of nodes exclude. If randomNodes, then this child node is selected uniformly at random from all candidates.
        """
        child = None
        for c in self.successors(node):
            if c not in exclude:
                if not randomNodes:
                    return c
                elif child == None or random.getrandbits(1):
                    # As there are at most two children, we can simply replace the previous child with probability .5 to get a random parent
                    child = c
        return child

    def parent(self, node, exclude=[], randomNodes=False):
        """
        Finds a parent of a node in a network.

        :param node: a node in the network.
        :param exclude: a set of nodes of the network.
        :param randomNodes: a boolean value.
        :return: a parent of node that is not in the set of nodes exclude. If randomNodes, then this parent is selected uniformly at random from all candidates.
        """
        parent = None
        for p in self.predecessors(node):
            if p not in exclude:
                if not randomNodes:
                    return p
                elif parent == None or random.getrandbits(1):
                    # As there are at most two parents, we can simply replace the previous parent with probability .5 to get a random parent
                    parent = p
        return parent


class RearrangementProblem(object):
    def __init__(self, network1, network2, move_type):
        self.network1 = network1
        self.network2 = network2
        self.move_type = move_type

    @staticmethod
    def same_labels(node1_attr, node2_attr):
        return node1_attr["label"] == node2_attr["label"]

    def check_solution(self, seq_moves, isomorphism=None):

        network1_copy = copy(network1)
        network1_copy.apply_move_sequence(seq_moves)
        
        if not isomorphism:
            return nx.is_isomorphic(network1_copy, network_2, node_match=self.same_labels)

        for corr in isomorphism:
            if not self.same_labels(network1_copy.nodes[corr[0]],network2.nodes[corr[1]]):
                return False
        isom_dict = {x[0]:x[1] for x in isomorphism}
        return nx.is_isomorphic(network1_copy, network_2, node_match=(lambda x,y: isom_dict[x]==y))

class Move(object):
    class Type:
        NONE = 0
        TAIL = 1
        HEAD = 2
        RSPR = 3

    def __init__(self, move_tuple):
        try:
            # horizontal move
            self.moving_node = move_tuple[3]
            self.target = move_tuple[2]
            self.moving_edge = move_tuple[1]
            self.origin = move_tuple[0]
            if self.moving_node == self.moving_edge[0]:
                self.type = self.Type.TAIL
            else:
                self.type = self.Type.HEAD
        except:
            try:
                # TODO Write vertical move paring
                raise InvalidMoveError
            except:
                raise InvalidMoveError


class Move_Sequence(object):
    def __init__(self, moves_string):
        self.move_sequence = ast.literal_eval(moves_string)
        move_types_tails_boolean = [
            move == Move.Type.TAIL for move in self.move_sequence
        ]
        self.head_used = len(move_sequence) > 0 and not all(move_types_tails_boolean)
        self.tail_used = len(move_sequence) > 0 and any(move_types_tails_boolean)
