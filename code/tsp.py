from itertools import chain, combinations


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