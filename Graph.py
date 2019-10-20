from math import sqrt
from queue import PriorityQueue
from collections import defaultdict
from typing import Set, List, Iterator
from itertools import cycle
from pprint import pprint, pformat

class Node:
    def __init__(self, id, x, y):
        self.id: str = str(id)
        self.x = int(x)
        self.y = int(y)

        self.neighbours = []
        
    def __hash__(self):
        return int(self.id)
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __repr__(self):
        return f"Node {self.id}: ({self.x},{self.y})"

class Edge:
    """ Representing a bidirectional edge. """
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2

        self.weight = self.dist(n1, n2)

    def dist(self, a, b):
        """ Euclidean dist between 2D coords """
        return sqrt((a.x - b.x)**2 + (a.y-b.y)**2)
    
    def contains(self, node):
        """ Determines if a target node is included in this edge """
        return self.n1 == node or self.n2 == node

    def nodes(self):
        return (self.n1, self.n2)

    def reverse(self):
        return Edge(self.n2, self.n1)

    def __hash__(self):
        """ Hash the same whether n1 or n2 are switched. """
        if self.n1.id < self.n2.id:
            return hash(str(self.n1.id+self.n2.id))
        return hash(str(self.n2.id+self.n1.id))
    
    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return self.weight == other.weight
    
    def __lt__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return self.weight < other.weight

    def __le__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return self.weight <= other.weight

    def __gt__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return self.weight > other.weight

    def __ge__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return self.weight >= other.weight
    
    def __repr__(self):
        return f"Edge {self.n1.id} -> {self.n2.id}, w = {self.weight}"

class Graph:
    def __init__(self, nodes):
        self.create_node_dict(nodes)

        self.adjlist = defaultdict(set)

        self.mst = set()
        self.mst_cost = 0

    def create_node_dict(self, nodes):
        if not nodes:
            nodes = self.nodes
        self.nodes = dict(zip([node.id for node in nodes], nodes))  

    def populate(self, edgelist=None):
        """ Create adjacency list for default=mst or another list of Edges """
        if not edgelist:
            edgelist = self.mst
        for edge in edgelist:
            self.adjlist[edge.n1.id].add(edge.n2.id)
            self.adjlist[edge.n2.id].add(edge.n1.id)

        # # Edges are the in-betweens...meaning to convert to num. nodes, we add one
        # assert len(self.adjlist) == len(self.mst)+1

    def build_MST(self):
        """ Prim's algorithm """
        fringe = PriorityQueue()

        visited: Set[str] = set() # Store ids of visited nodes
        
        # mark an arbitrary node as visited and process its neighbours
        currn = list(self.nodes.values())[0]
        
        visited.add(currn.id)
        
        for neigh in self.nodes.values():
            fringe.put(Edge(currn, neigh))
        
        # Walk and create the MST
        while not fringe.empty():
            curr_edge = fringe.get()
            
            if curr_edge in self.mst or curr_edge.n2.id in visited:
                continue
            
            # Record the walk from node1 to node2   
            self.mst.add(curr_edge)
            visited.add(curr_edge.n1.id)
            visited.add(curr_edge.n2.id)

            self.mst_cost += curr_edge.weight
            currn = curr_edge.n2

            for neigh in self.nodes.values():
                if neigh != currn:
                    fringe.put(Edge(currn, neigh))

        assert len(visited) == len(self.nodes), "Not all nodes are represented in this MST"
        
        return (self.mst, self.mst_cost)

    def get_node(self, id):
        """ Returns Node object given an id, or None if non existing """
        if id in self.nodes:
            return self.nodes[id]
        return None
    
    def __str__(self):
        return pformat(self.adjlist)

    def __repr__(self):
        return pformat(self.adjlist)

class Path:
    def __init__(self, edgelist):
        self.path: List[Edge] = edgelist
        self.cycle: Iterator[Edge] = cycle(edgelist)

        self.adjlist = defaultdict(list)
        self.cost = 0
        for edge in edgelist:
            self.adjlist[edge.n1].append(edge.n2)
            self.cost += edge.weight

        self.nodes = list(self.adjlist.keys())

    def next_edge(self, node) -> Edge:
        return Edge(node, self.adjlist[node][0])

    def segment(self, start, end):
        seg = []
        currn = start
        
        while currn != end:
            seg.append(self.next_edge(currn))
            currn = self.adjlist[currn][0]
        return Path(seg)
            
    def reverse(self):
        return Path([e.reverse() for e in self.path][::-1])

    def clone(self):
        return Path(self.path)

    def __str__(self):
        return pformat(self.path)

    def __repr__(self):
        return pformat(self.path)

def readTSP(tspfile):
    nodes = []
    read_coords = False

    dim = 0
    with open(tspfile) as f:
        for line in f:
            if "NODE_COORD_SECTION" in line:
                read_coords = True
                continue
            elif "DIMENSION" in line:
                dim = int(line.split()[-1])
                continue
        
            if read_coords and 'EOF' not in line:
                nodes.append(Node(*line.split()))
    
    assert dim == len(nodes)
    return nodes

