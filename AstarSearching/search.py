"""This module contains classes and functions related to graph
search. It is specifically written for the course COSC367:
Computational Intelligence. Most of the code here is abstract.  The
normal usage would be to write concrete subclasses for particular
problems.

Author: Kourosh Neshatian
Last modified: 20 Jul 2014
"""

from abc import ABCMeta, abstractmethod 
from collections import namedtuple

def generic_search(graph, frontier):
    """Implements a generic graph search algorithm (Figure 3.4 of the
    textbook). The actual search behaviour will depend on the type of
    the frontier object. If the function halts it returns either a
    solution (a path) to a goal node/state (if there exist one) or it
    returns None.

    """

    for node in graph.starting_nodes():
        frontier.add((Arc(None, node, "no action", 0),))
    
    solution = None
    for path in frontier:
        node_to_expand = path[-1].head

        if graph.is_goal(node_to_expand):
            solution = path
            break

        for arc in graph.outgoing_arcs(node_to_expand):
            frontier.add(path + (arc,))

    return solution


class Arc(namedtuple('Arc', 'tail, head, label, cost')):
    """Represents an arc in a graph.

    Keyword arguments:
    tail -- the source node (state)
    head -- the destination node (state)
    label -- a string describing the action that must be taken in
             order to get from the source state to the destination state.
    cost -- a number that specifies the cost of the action
    """


class Graph(metaclass=ABCMeta):
    """This is an abstract class for graphs. It cannot be directly
    instantiated. You should define a subclass of this class
    (representing a particular problem) and implement the expected
    methods."""

    @abstractmethod
    def is_goal(self, node):
        """Returns true if the given node is a goal state."""

    @abstractmethod
    def starting_nodes():
        """Return a sequence of starting nodes. Often there is only one
        starting node but even then the function returns a sequence
        with one element. It can be implemented as an iterator.

        """

    @abstractmethod
    def outgoing_arcs(self, tail_node):
        """Given a node it returns a sequence of arcs (Arc objects)
        which correspond to the actions that can be taken in that
        state (node)."""

    def estimated_cost_to_goal(self, node):
        """Return the estimated cost to a goal node from the given
        state. This function is usually implemented when there is a
        single goal state. The function is used as a heuristic in
        search. The implementation should make sure that the heuristic
        meets the required criteria for heuristics."""

        raise NotImplementedError


class ExplicitGraph(Graph):
    """This is a concrete subclass of Graph where vertices and edges
     are explicitly enumerated. Objects of this type are useful for
     testing graph algorithms."""

    def __init__(self, nodes, edge_list, starting_list, goal_nodes, estimates=None):
        """Initialises an explicit graph.
        Keyword arguments:
        nodes -- a set of nodes
        edge_list -- a sequence of tuples in the form (tail, head) or 
                     (tail, head, cost)
        starting_list -- the list of starting nodes (states)
        goal_node -- the set of goal nodes (states)
        """

        # A few assertions to detect possible errors in
        # instantiation. These assertions are not essential to the
        # class functionality.
        assert all(tail in nodes and head in nodes for tail, head, *_ in edge_list)\
           , "edges must link two existing nodes!"
        assert all(node in nodes for node in starting_list),\
            "The starting_states must be in nodes."
        assert all(node in nodes for node in goal_nodes),\
            "The goal states must be in nodes."

        self.nodes = nodes      
        self.edge_list = edge_list
        self.starting_list = starting_list
        self.goal_nodes = goal_nodes
        self.estimates = estimates

    def starting_nodes(self):
        """Returns (via a generator) a sequece of starting nodes."""
        for starting_node in self.starting_list:
            yield starting_node

    def is_goal(self, node):
        """Returns true if the given node is a goal node."""
        return node in self.goal_nodes

    def outgoing_arcs(self, node):
        """Returns a sequence of Arc objects corresponding to all the
        edges in which the given node is the tail node. The label is
        automatically generated."""

        for edge in self.edge_list:
            tail, head = edge[:2]
            if tail == node:
                cost = edge[2] if len(edge) > 2 else 1
                yield Arc(tail, head, str(tail) + '->' + str(head), cost)



class Frontier(metaclass = ABCMeta):
    """This is an abstract class for frontier classes. It outlines the
    methods that must be implemented by a concrete subclass. Concrete
    subclasses will determine the search strategy.

    """


    @abstractmethod
    def add(self, path):
        """Adds a new path to the frontier. A path is a sequence (tuple) of
        Arc objects. You should override this method.

        """

    @abstractmethod
    def __iter__(self):
        """Returns a generator. The generator selects and removes a path from
        the frontier and returns it. A path is a sequence (tuple) of
        Arc objects. Override this method according to the desired
        search strategy.

        """



def print_actions(path):
    """Given a path (a sequence of Arc objects), prints the actions
    (arc labels) that need to be taken and the total cost of those
    actions. The path is usually a solution (a path from the starting
    node to a goal node."""

    if path:
        print("Actions:")
        for arc in path[1:-1]:
            print("  {},".format(arc.label))
        print("  {}.".format(path[-1].label))
        print("Total Cost:", sum(arc.cost for arc in path))
    else:
        print("There is no solution!")


