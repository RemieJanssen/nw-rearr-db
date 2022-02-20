import ast
from copy import deepcopy
from enum import Enum
from random import getrandbits

import networkx as nx


class InvalidMoveDefinition(Exception):
    pass


class InvalidMove(Exception):
    pass


def same_labels(node1_attr, node2_attr):
    return node1_attr.get("label", None) == node2_attr.get("label", None)


def is_isomorphic(nw1, nw2, partial_isomorphism=None):
    nw1 = deepcopy(nw1)
    nw2 = deepcopy(nw2)

    partial_isomorphism = partial_isomorphism or []
    for i, corr in enumerate(partial_isomorphism):
        if not same_labels(nw1.nodes[corr[0]], nw2.nodes[corr[1]]):
            return False
        nw1.nodes[corr[0]]["label"] = f"{i}_isom_label"
        nw2.nodes[corr[1]]["label"] = f"{i}_isom_label"

    return nx.is_isomorphic(nw1, nw2, node_match=same_labels)


class Network(nx.DiGraph):
    def __init__(self, *args, **kwargs):
        edges = kwargs.get("edges", [])
        super().__init__(edges, *args, **kwargs)
        self.add_nodes_from(kwargs.get("nodes", []))
        for label in kwargs.get("labels", []):
            self.nodes[label[0]]["label"] = label[1]

    def apply_move(self, move):
        """
        Apply a move to the network.
        returns True if successful, and False otherwise.
        """
        self.check_valid(move)

        if move.move_type in [MoveType.TAIL, MoveType.HEAD]:
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
            return
        if move.move_type in [MoveType.NONE]:
            return
        # TODO implement vertical moves
        raise InvalidMove("only tail or head moves are currently valid.")

    def apply_move_sequence(self, seq_moves):
        for move in seq_moves:
            self.apply_move(move)

    def check_valid(self, move):
        """
        Checks whether a move is valid.

        :param move: a move of type Move
        :return: void
        """
        if move.move_type == MoveType.NONE:
            return

        if move.is_type(MoveType.RSPR):
            if move.moving_edge == move.target:
                raise InvalidMove("moving edge must not be the target edge.")
            if not self.check_movable(move.moving_edge, move.moving_node):
                raise InvalidMove("the edge is not movable")
            if move.is_type(MoveType.TAIL):
                if nx.has_path(self, move.moving_edge[1], move.target[0]):
                    raise InvalidMove("the move would create a cycle")
                if move.target[1] == move.moving_edge[1]:
                    raise InvalidMove("the move would create parallel edges")
                return
            if move.is_type(MoveType.HEAD):
                if nx.has_path(self, move.target[1], move.moving_edge[0]):
                    raise InvalidMove("the move would create a cycle")
                if move.target[0] == move.moving_edge[0]:
                    raise InvalidMove("the move would create parallel edges")
            return
        raise InvalidMove("Only rSPR moves are supported currently")

    def check_movable(self, moving_edge, moving_node):
        """
        Checks whether an endpoint of an edge is movable.

        :param moving_edge: an edge.
        :param moving_node: a node, specifically, an endpoint of the moving_edge.
        :return: True if the endpoint of the edge is movable, False otherwise.
        """
        if moving_node == moving_edge[0]:
            # Tail move
            if self.in_degree(moving_node) in (0, 2):
                # cannot move the tail if it is a reticulation or root
                return False
        elif moving_node == moving_edge[1]:
            # Head move
            if self.out_degree(moving_node) in (0, 2):
                # cannot move the head if it is a tree node or leaf
                return False
        else:
            # Moving endpoint is not part of the moving edge
            return False
        # Now check for triangles, by finding the other parent and child of the moving endpoint
        parent_of_moving_node = self.parent(
            moving_node, exclude=[moving_edge[0]]
        )
        child_of_moving_node = self.child(
            moving_node, exclude=[moving_edge[1]]
        )
        # if there is an edge from the parent to the child, there is a triangle
        # Otherwise, it is a movable edge
        return not self.has_edge(parent_of_moving_node, child_of_moving_node)

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
                elif child is None or getrandbits(1):
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
                elif parent is None or getrandbits(1):
                    # As there are at most two parents, we can simply replace the previous parent with probability .5 to get a random parent
                    parent = p
        return parent


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


class MoveType(str, Enum):
    NONE = "NONE"
    TAIL = "TAIL"
    HEAD = "HEAD"
    RSPR = "RSPR"
    VPLU = "VPLU"  # not currently in use
    VMIN = "VMIN"  # not currently in use
    VERT = "VERT"


class Move(object):
    def __init__(self, *args, **kwargs):
        try:
            self.move_type = kwargs["move_type"]
        except KeyError:
            raise InvalidMoveDefinition("Missing move_type.")

        # None type move
        if self.move_type == MoveType.NONE:
            return

        # TAIL/HEAD move (i.e. RSPR/horizontal)
        if self.move_type == MoveType.RSPR:
            raise InvalidMoveDefinition(
                "rSPR moves must be defined as moves of type tail or head."
            )
        if self.move_type in [MoveType.TAIL, MoveType.HEAD]:
            try:
                self.origin = kwargs["origin"]
                self.moving_edge = kwargs["moving_edge"]
                self.target = kwargs["target"]
            except KeyError:
                raise InvalidMoveDefinition(
                    "Missing one of origin, moving_edge, or target."
                )

            if self.move_type == MoveType.TAIL:
                self.moving_node = self.moving_edge[0]
            else:
                self.moving_node = self.moving_edge[1]

            return

        # TODO Write vertical move parsing
        if self.move_type == MoveType.VPLU:
            try:
                self.start_edge = kwargs["start_edge"]
                self.end_edge = kwargs["end_edge"]
                self.start_node = kwargs["start_node"]
                self.end_node = kwargs["end_node"]
            except KeyError:
                raise InvalidMoveDefinition(
                    "Missing one of start_edge, end_edge, start_node, or end_node."
                )
            return

    def is_type(self, move_type):
        if (
            self.move_type == MoveType.NONE
            or (
                move_type == MoveType.RSPR
                and self.move_type in [MoveType.TAIL, MoveType.HEAD]
            )
            or (
                move_type == MoveType.VERT
                and self.move_type in [MoveType.VPLU, MoveType.VMIN]
            )
        ):
            return True
        return move_type == self.move_type


class Move_Sequence(object):
    def __init__(self, moves_string):
        self.move_sequence = ast.literal_eval(moves_string)
        move_types_tails_boolean = [
            move == MoveType.TAIL for move in self.move_sequence
        ]
        self.head_used = len(self.move_sequence) > 0 and not all(
            move_types_tails_boolean
        )
        self.tail_used = len(self.move_sequence) > 0 and any(
            move_types_tails_boolean
        )
