###
### graph.py
###

class Graph(object):
    """
    Represents a directed graph.
    """

    def __init__(self):
        self._nodes = {}

    def add_node(self, node):
        """
        If node is already in the graph, returns False and do not modify the graph.
        Otherwise, adds node to the graph and returns True.
        """
        if node in self._nodes:
            return False
        self._nodes[node] = set()
        return True

    def has_node(self, node):
        """
        Returns True iff node is a node in the graph.
        """
        return node in self._nodes

    def add_edge(self, node1, node2):
        """
        Requires: node1 and node2 are nodes in self.
        Modifies: self
        Adds an edge from node1 to node2 to self.
        """
        assert self.has_node(node1)
        assert self.has_node(node2)
        self._nodes[node1].add(node2)

    def get_nodes(self):
        """
        Returns a frozenset containing the nodes in the graph.
        """
        return frozenset(self._nodes)

    def get_outlinks(self, node):
        """
        Requires: node is a node in self.
        Returns a frozenset of the nodes to which node is connected.
        """
        assert self.has_node(node)
        return frozenset(self._nodes[node])

    def get_inlinks(self, target):
        """
        Requires: node is a node in self.
        Returns a set of the nodes that are connected by an edge to node.
        """
        return set(filter(lambda node: target in self.get_neighbors(node), self._nodes))
    
    def __str__(self):
        """
        Returns a string representation of the graph. 
        """
        res = "<graph "
        res += '; '.join(map(lambda node: str(node) + " -> "  
                             + ", ".join(map(lambda target: str(target),
                                                        self.get_neighbors(node))),
                             self._nodes))
        res += ">"
        return res

if __name__ == '__main__':
    print "Testing graph..."
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_node("C")
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("B", "A")
    print g
    assert g.get_neighbors("A") == frozenset(["B"])
    assert len(g.get_nodes()) == 3
    assert g.get_neighbors("B") == frozenset(["A", "C"])
    assert g.get_inlinks("A") == set(["B"])
    g.add_edge("C", "A")
    assert g.get_inlinks("A") == set(["B", "C"])
    print "Finished tests."
