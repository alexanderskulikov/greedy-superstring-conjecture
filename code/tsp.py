from itertools import chain, combinations
import math
import networkx as nx


# This function takes as input a graph g.
# The graph may be directed and may have arcs with multiplicities.


# This function returns all the subsets of the given set s in the increasing order of their sizes.
def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


# This function finds uses the dynamic programming approach
# to find an optimal Hamiltonian path starting at the vertex start.
def dynamic_programming(g, begin):
    # n is the number of vertices.
    n = g.number_of_nodes()

    # The variable power now contains a tuple for each subset
    # of the set {0, ..., n-1} \ {begin}.
    power = powerset([x for x in range(n) if x != begin])
    # The variable T is a dictionary, where the element T[s, end] for a set s and an integer
    # end equals the shortest path going through each vertex from s exactly once,
    # starting at the vertex start and ending at the vertex end.
    # Thus, for convenience, we will always exclude the element begin from the set s.
    # Note that end must be in s.
    # In order to reconstruct an optimal solution, we also store the values of parents:
    # p[s, end] is the last vertex before end in an optimal path going through s.
    T = {}
    p = {}
    # For every vertex end != start we set T[ tuple with the element end only, end]
    # to the weight of the edge from start to end.
    for end in range(n):
        if end != begin:
            # Syntactic note: In Python, we define a tuple of length 1
            # that contains the element end as (end,) *with comma*.
            T[(end,), end] = g[begin][end]['weight']
            p[(end,), end] = begin

    # For every subset s of {0,...,n-1} \ {begin}
    for s in power:
        # We have already initialized the elements of T indexed by sets of size 1, so we skip them.
        if len(s) > 1:
            # For every vertex end from s which we consider as the ending vertex
            # of a path going through vertices from s.
            for end in s:
                if begin != end:
                    # Define the tuple which contains all elements from s without *the last vertex* end.
                    t = tuple([x for x in s if x != end])
                    # Now we compute the optimal value of a path which visits all vertices from s,
                    #  and ends at the vertex end.
                    mn, idx = min((T[t, i] + g[i][end]['weight'], i) for i in t)
                    T[s, end] = mn
                    p[s, end] = idx

    # Compute the weight of on optimal Hamiltonian path.
    # all is the set of all vertices except begin.
    all = tuple([x for x in range(n) if x != begin])
    opt, finish = min((T[all, end], end) for end in range(n) if end != begin)

    # Compute an optimal Hamiltonian path.
    path = []
    node = finish
    s = all
    while node != begin:
        path.append(node)
        next = p[s, node]
        s = tuple([x for x in s if x != node])
        node = next
    path.append(begin)
    return opt, list(reversed(path))


coordinates = {0: [(178, 212), (287, 131), (98, 156)],
                   1: [(231, 91), (7, 21), (226, 276), (11, 266)],
                   2: [(174, 25), (129, 99), (268, 212), (211, 209), (156, 82)],
                   3: [(199, 59), (152, 117), (68, 87), (281, 161), (11, 53), (254, 227)],
                   4: [(44, 105), (137, 277), (53, 202), (93, 296), (156, 214), (187, 137), (147, 195)],
                   5: [(162, 137), (122, 177), (249, 49), (37, 127), (13, 277), (164, 293), (270, 42), (135, 123)],
                   6: [(165, 117), (13, 241), (97, 260), (287, 299), (273, 19), (138, 22), (120, 25), (10, 286),
                       (95, 150)],
                   7: [(88, 106), (248, 67), (251, 24), (124, 221), (136, 148), (262, 88), (179, 45), (60, 188),
                       (272, 99), (30, 107)],
                   8: [(181, 243), (101, 143), (100, 216), (167, 15), (37, 201), (163, 226), (2, 42), (35, 73),
                       (85, 116), (142, 235), (200, 18)]}


def dist(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def path_length(g, path):
        assert len(path) == g.number_of_nodes()
        return sum(g[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))


def read_graph(test_index):
        g = nx.DiGraph()
        coors = coordinates[test_index]
        n = len(coors)
        for i in range(n):
            for j in range(n):
                g.add_edge(i, j, weight=dist(coors[i][0], coors[i][1], coors[j][0], coors[j][1]))
        return g


g = read_graph(0)
dynamic_programming(g, 0)

