import random
from copy import deepcopy

import networkx as nx

from .exceptions import CannotComputeError, InvalidMove, InvalidReduction
from .movetype import MoveType
from .networkclasses import NetworkClass

LEVEL_BOUNDARY = 0.05
TREE_CHILD_JITTER = 0.03
RETICULATION_CHILD_JITTER = 0.06


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

    @property
    def leaves(self):
        return set([node for node in self.nodes if self.is_leaf(node)])

    @property
    def roots(self):
        return set([node for node in self.nodes if self.is_root(node)])

    @property
    def reticulation_number(self):
        return sum([max(self.in_degree(node) - 1, 0) for node in self.nodes])

    def clip_to_playing_field(self, pos):
        return max(
            min(pos, 1.0 - LEVEL_BOUNDARY),
            LEVEL_BOUNDARY,
        )

    def calculate_node_positions(self):
        # determine the x-pos of the leaves with a dfs, other nodes follow more or less
        # y positions are computed depending on children's y coordinates
        # all positions must lie within the unit square

        # dfs for x positions
        nodes_done = set()
        ordered_sinks = []
        for r in self.roots:
            curr_nodes = [r]
            while curr_nodes:
                current_node = curr_nodes.pop()
                if current_node in nodes_done:
                    continue
                nodes_done.add(current_node)
                if self.out_degree(current_node) == 0:
                    ordered_sinks.append(current_node)
                    continue
                curr_nodes += list(self.successors(current_node))

        # bfs
        nodes_done = set(ordered_sinks)
        number_of_sinks = len(ordered_sinks)
        node_x_positions = {
            node: LEVEL_BOUNDARY
            + (1.0 - 2 * LEVEL_BOUNDARY) * (i + 1) / (number_of_sinks + 1)
            for i, node in enumerate(ordered_sinks)
        }
        print(node_x_positions)
        node_y_positions = {node: 0 for node in ordered_sinks}
        current_nodes = [
            node
            for node in self.nodes
            if node not in nodes_done
            and all([x in nodes_done for x in self.successors(node)])
        ]

        while current_nodes:
            current_node = current_nodes.pop()
            nodes_done.add(current_node)

            children_xs = [
                node_x_positions[node]
                for node in self.successors(current_node)
            ]

            jitter = TREE_CHILD_JITTER
            if (
                self.out_degree(current_node) == 1
                and self.out_degree(self.child(current_node)) == 1
            ):
                jitter = RETICULATION_CHILD_JITTER

            node_x_positions[current_node] = self.clip_to_playing_field(
                float(sum(children_xs)) / len(children_xs)
                + (random.random() - 0.5) * (2 * jitter)
            )
            children_ys = [
                node_y_positions[node]
                for node in self.successors(current_node)
            ]
            node_y_positions[current_node] = max(children_ys) + 1

            for parent in self.predecessors(current_node):
                if all(
                    [child in nodes_done for child in self.successors(parent)]
                ):
                    current_nodes.append(parent)

        max_y = max(list(node_y_positions.values()) + [0])
        node_pos_list = []
        max_y_jitter = (1.0 - 2 * LEVEL_BOUNDARY) / (max_y + 1) / 2
        tc_jitter_y = min(TREE_CHILD_JITTER, max_y_jitter)
        retic_jitter_y = min(RETICULATION_CHILD_JITTER, max_y_jitter)
        for node in self.nodes:
            jitter = tc_jitter_y
            if (
                self.out_degree(current_node) == 1
                and self.out_degree(self.child(current_node)) == 1
            ):
                jitter = retic_jitter_y

            y_pos = self.clip_to_playing_field(
                LEVEL_BOUNDARY
                + (random.random() - 0.5) * (2 * jitter)
                + (1.0 - 2 * LEVEL_BOUNDARY)
                * (1.0 - node_y_positions[node] / max_y)
            )

            node_pos_list.append([node, node_x_positions[node], y_pos])
        return node_pos_list

    def is_second_in_reducible_pair(self, x):
        px = self.parent(x)
        cpx = self.child(px, exclude=[x])
        if cpx is None:
            return False
        if self.is_leaf(cpx):
            return (cpx, x)
        if self.is_reticulation(cpx):
            ccpx = self.child(cpx)
            if self.is_leaf(ccpx):
                return (ccpx, x)
        return False

    def reduce_pair(self, pair):
        x, y = pair
        if not self.is_leaf(x) or not self.is_leaf(y):
            raise InvalidReduction("Can only reduce reducible leaf pairs.")
        px = self.parent(x)
        py = self.parent(y)
        ppy = self.parent(py)
        if px == py:
            if self.out_degree(px) == 2:
                self.remove_edges_from([(ppy, py), (py, y)])
                self.add_edge(ppy, y)
            self.remove_edge(py, x)
            return "cherry"
        if py in self.predecessors(px):
            ppx = self.parent(px, exclude=[py])
            if self.out_degree(py) == 2:
                self.remove_edges_from([(ppy, py), (py, y)])
                self.add_edge(ppy, y)
            if self.in_degree(px) == 2:
                self.remove_edges_from([(ppx, px), (px, x)])
                self.add_edge(ppx, x)
            self.remove_edge(py, px)
            return "reticulated_cherry"
        raise InvalidReduction("Trying to reduce an irreducible pair.")

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
            if c not in exclude:
                if not randomNodes:
                    return c
                elif child is None or random.getrandbits(1):
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

    def is_reticulation(self, node):
        return self.out_degree(node) <= 1 and self.in_degree(node) > 1

    def is_leaf(self, node):
        return self.out_degree(node) == 0 and self.in_degree(node) > 0

    def is_root(self, node):
        return self.in_degree(node) == 0

    def is_tree_node(self, node):
        return self.out_degree(node) > 1 and self.in_degree(node) <= 1

    def is_endpoint_of_w_fence(self, node):
        if not self.is_reticulation(node):
            return False
        previous_node = node
        current_node = self.child(node)
        currently_at_fence_top = False
        while True:
            if self.is_leaf(current_node):
                return False
            if self.is_reticulation(current_node):
                if currently_at_fence_top:
                    return True
                next_node = self.parent(current_node, exclude=[previous_node])
            if self.is_tree_node(current_node):
                if not currently_at_fence_top:
                    return False
                next_node = self.child(current_node, exclude=[previous_node])
            previous_node, current_node = current_node, next_node
            currently_at_fence_top = not currently_at_fence_top

    ## network classes

    def check_class(self, network_class):
        if network_class == NetworkClass.BI:
            return self.is_binary()
        if network_class == NetworkClass.TC:
            return self.is_tree_child()
        if network_class == NetworkClass.OR:
            return self.is_orchard()
        if network_class == NetworkClass.SF:
            return self.is_stack_free()
        if network_class == NetworkClass.TB:
            return self.is_tree_based()
        raise CannotComputeError("network_class is not defined")

    def is_binary(self):
        binary_node_types = [
            [0, 1],  # root
            [0, 2],  # root
            [1, 2],  # tree node
            [2, 1],  # reticulation
            [1, 0],  # leaf
        ]
        for node in self.nodes:
            degrees = [self.in_degree(node), self.out_degree(node)]
            if degrees not in binary_node_types:
                return False
        return True

    def is_tree_child(self):
        for node in self.nodes:
            if self.is_leaf(node):
                continue
            if all(
                [
                    self.is_reticulation(child)
                    for child in self.successors(node)
                ]
            ):
                return False
        return True

    def is_stack_free(self):
        for node in self.nodes:
            if self.is_reticulation(node) and any(
                [
                    self.is_reticulation(child)
                    for child in self.successors(node)
                ]
            ):
                return False
        return True

    def is_tree_based(self):
        if not self.is_binary():
            raise CannotComputeError(
                "tree-basedness cannot be computed for non-binary networks yet."
            )

        if len(self) > 0 and not nx.is_weakly_connected(self):
            return False

        if len(self.roots) > 1:
            return False

        for node in self.nodes:
            if self.is_endpoint_of_w_fence(node):
                return False
        return True

    def is_orchard(self):
        if len(self) == 0:
            return True
        leaves = self.leaves
        root = list(self.roots)[0]

        # make a copy and fix a root edge
        network_copy = deepcopy(self)
        if network_copy.out_degree(root) > 1:
            new_node = -1
            while new_node in network_copy.nodes:
                new_node -= 1
            network_copy.add_edge(new_node, root)

        # try to reduce the network copy
        done = False
        while not done:
            checked_all_leaves = True
            for leaf in leaves:
                print("leaf", leaf)
                pair = network_copy.is_second_in_reducible_pair(leaf)
                print("pair", pair)
                if pair:
                    reduced = network_copy.reduce_pair(pair)
                    if reduced == "cherry":
                        leaves.remove(pair[0])
                    checked_all_leaves = False
                    break
            if len(network_copy.edges) == 1:
                return True
            done = checked_all_leaves
        return False
