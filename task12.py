from typing import List
import networkx as nx

class Worker:
    def __init__(self, name, current_shift: int, preferences: List[int]):
        self.name = name
        self.current_shift = current_shift
        self.preferences = preferences
        self.wanted_shift = preferences[0]

    def value(self, index: int):
        return self.preferences[index]

    def delete_first(self):
        del (self.preferences[0])
        self.wanted_shift = self.preferences[0]


def exchange_shifts(workers: List[Worker]):
    # init graph
    g = nx.DiGraph()
    g.add_nodes_from(workers)  # worker node
    g.add_nodes_from([0, len(workers) - 1])  # shift node

    for w in workers:
        g.add_edge(w.current_shift, w)  # add edge from shift to worker
        g.add_edge(w, w.wanted_shift)  # add edge from worker to wanted shift

    while not nx.is_empty(g):
        # find cycle and update shifts and remove nodes
        for cycle in nx.simple_cycles(g):
            for node in cycle:
                if not isinstance(node, int):  # go on the workers and match shifts
                    if not node.wanted_shift == node.current_shift:  # if the shift was switched
                        print(node.name, "moves from shift", node.current_shift, "to shift", node.wanted_shift)
                    else:
                        print(node.name, "stays with shift", node.current_shift)
            g.remove_nodes_from(cycle)

        # update new wanted shifts
        for w in list(g.nodes):
            if not isinstance(w, int):
                while not g.has_node(w.wanted_shift):  # search the first shift that exists
                    w.delete_first()
                g.add_edge(w, w.wanted_shift)  # add edge from worker to wanted shift


if __name__ == "__main__":
    import doctest
    doctest.testfile("test.txt", verbose=True)
