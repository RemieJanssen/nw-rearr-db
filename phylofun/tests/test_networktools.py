from django.test import TestCase
from phylofun.network_tools.base import Network
from phylofun.network_tools.base import Move
from phylofun.network_tools.base import MoveType
import networkx as nx

class NetworkTestCase(TestCase):
    def test_empty_network(self):
        network = Network()
        assert list(network.nodes) == []

    def test_nodes_only_network(self):
        network = Network()
        node_list = [0,1,2]
        network.add_nodes_from(node_list)
        assert list(network.nodes) == node_list


class MoveTestCase(TestCase):
    def test_make_move_head(self):
        m = Move(((0,2),(3,1),(4,5),1))
        assert m.type == MoveType.HEAD
