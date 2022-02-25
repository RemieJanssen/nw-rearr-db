import random
from copy import deepcopy

import networkx as nx

from .exceptions import InvalidMove
from .movetype import MoveType


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
            if not self.has_edge(
                move.origin[0], move.moving_node
            ) or not self.has_edge(move.moving_node, move.origin[1]):
                # also catches wrong endpoint type:
                # e.g.: reticulation moving_node for tail move
                raise InvalidMove(
                    "origin does not match parent and child or moving_endpoint"
                )
            if self.has_edge(move.origin[0], move.origin[1]):
                raise InvalidMove("removal creates parallel edges")

            if move.is_type(MoveType.TAIL):
                if nx.has_path(self, move.moving_edge[1], move.target[0]):
                    raise InvalidMove("reattachment would create a cycle")
                if move.target[1] == move.moving_edge[1]:
                    raise InvalidMove("reattachment creates parallel edges")
                return
            # move.is_type(MoveType.HEAD)
            if nx.has_path(self, move.target[1], move.moving_edge[0]):
                raise InvalidMove("reattachment would create a cycle")
            if move.target[0] == move.moving_edge[0]:
                raise InvalidMove("reattachment creates parallel edges")
            return

        raise InvalidMove("Only rSPR moves are supported currently")

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
            print(c)
            if c not in exclude:
                if not randomNodes:
                    return c
                elif child is None or random.getrandbits(1):
                    print("yo")
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
                elif parent is None or random.getrandbits(1):
                    # As there are at most two parents, we can simply replace the previous parent with probability .5 to get a random parent
                    parent = p
        return parent
