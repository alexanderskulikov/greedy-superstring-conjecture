from itertools import chain, combinations


# This function takes as input a graph g.
# The graph may be directed and may have arcs with multiplicities.


# This function returns all the subsets of the given set s in the increasing order of their sizes.
def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


# This function finds an optimal Hamiltonian path using the dynamic programming approach.
def dynamic_programming(g):
    # n is the number of vertices.
    n = g.number_of_nodes()

    # The variable power now contains a tuple for each subset of the set {0, ..., n-1}.
    power = powerset(range(n))
    # The variable T is a dictionary, where the element T[s, begin, end] for a set s and integers
    # begin and end equals the shortest path going through each vertex from s exactly once,
    # starting at the vertex begin and ending at the vertex end.
    # Note that begin and end must be in s.
    # In order to reconstruct an optimal solution, we also store the values of parents:
    # p[s, begin, end] is the last vertex before end in an optimal path through s.
    T = {}
    p = {}
    # For every pair of distinct vertices i and j, we set
    # T[ tuple with the two element i and j, i, i] to the weight of the arc from i to j.
    for begin in range(n):
        for end in range(n):
            if begin != end:
                T[(min(begin, end), max(begin, end)), begin, end] = g[begin][end]['weight']
                p[(min(begin, end), max(begin, end)), begin, end] = begin

    # For every subset s of [0,...,n-1]
    for s in power:
        # We have already initialized the elements of T indexed by sets of size 1, so we skip them.
        if len(s) > 2:
            # For every vertex start from s which we consider as the starting vertex
            # of a path going through vertices from s.
            for start in s:
                # For every vertex end from s which we consider as the ending vertex
                # of a path going through vertices from s.
                for end in s:
                    if start != end:
                        # Define the tuple which contains all elements from s without *the last vertex* end.
                        t = tuple([x for x in s if x != end])
                        # Now we compute the optimal value of a path which visits all vertices from s,
                        #  and ends at the vertex end.
                        mn, idx = min((T[t, start, i] + g[i][end]['weight'], i) for i in t if i != start)
                        T[s, start, end] = mn
                        p[s, start, end] = idx

    # Compute the weight of on optimal Hamiltonian path.
    opt, start, finish = min((T[tuple(range(n)), begin, end], begin, end)
                             for begin in range(n) for end in range(0, n) if end != begin)
    # Return an optimal Hamiltonian path.
    path = []
    node = finish
    s = tuple(range(n))
    while node != start:
        path.append(node)
        next = p[s, start, node]
        s = tuple([x for x in s if x != node])
        node = next
    path.append(start)
    return list(reversed(path))
