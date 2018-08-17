import networkx as nx
#from . import graph_drawer
import graph_drawer

__empty_node_name__ = "eps"
debug_print = False


def get_upper_indegree(graph, v):
    assert v != "" and v != __empty_node_name__
    if not graph.has_node(v):
        return 0

    upper_indegree = 0
    for u in graph.predecessors(v):
        if len(u) == len(v) + 1:
            upper_indegree += graph.number_of_edges(u, v)
    return upper_indegree


def get_upper_outdegree(graph, v):
    assert v != "" and v != __empty_node_name__
    if not graph.has_node(v):
        return 0

    upper_outdegree = 0
    for u in graph.successors(v):
        if len(u) == len(v) + 1:
            upper_outdegree += graph.number_of_edges(v, u)
    return upper_outdegree


def get_lower_indegree(graph, v):
    assert v != "" and v != __empty_node_name__
    if not graph.has_node(v):
        return 0

    lower_indegree = 0
    for u in graph.predecessors(v):
        if len(u) == len(v) - 1 or (len(v) == 1 and u == __empty_node_name__):
            lower_indegree += graph.number_of_edges(u, v)
    return lower_indegree


def get_lower_outdegree(graph, v):
    assert v != "" and v != __empty_node_name__
    if not graph.has_node(v):
        return 0

    lower_outdegree = 0
    for u in graph.successors(v):
        if len(u) == len(v) - 1 or (len(v) == 1 and u == __empty_node_name__):
            lower_outdegree += graph.number_of_edges(v, u)
    return lower_outdegree


def set_of_edges_to_superstring(graph):
    cycle = nx.eulerian_circuit(graph, 'eps')
    superstring = ''
    for cur, next in cycle:
        if next != 'eps' and (cur == 'eps' or len(next) > len(cur)):
            superstring += next[-1]
    return superstring


def construct_greedy_solution(strings, print_description=True, output_folder='output'):
    drawer = graph_drawer.GraphDrawer(strings, output_folder, print_description)
    greedy_graph = nx.MultiDiGraph()
    processed_nodes = []

    drawer.draw(greedy_graph, processed_nodes,
                description="initial hierarchical graph")
    drawer.draw(greedy_graph, processed_nodes,
                description="we first process input strings")

    for s in sorted(strings):
        pref = s[:-1] if s[:-1] != "" else "eps"
        suff = s[1:]  if s[1:]  != "" else "eps"

        processed_nodes.append(s)
        drawer.draw(greedy_graph, processed_nodes,
            "{} is an input string hence we add two bottom edges to it: {}->{}->{}".format(s, pref, s, suff)
                    )

        greedy_graph.add_edge(pref, s)
        greedy_graph.add_edge(s, suff)

        drawer.draw(greedy_graph, processed_nodes)

    drawer.draw(greedy_graph, processed_nodes,
        "we now process nodes from top to bottom in lexicographical ordering"
                )

    max_level = max(len(s) for s in strings)
    cur_level = max_level - 1

    while not greedy_graph.has_node("eps"):
        cur_level_vertices = sorted([v for v in greedy_graph.nodes() if len(v) == cur_level])
        cur_level -= 1

        for v in cur_level_vertices:
            processed_nodes.append(v)
            drawer.draw(greedy_graph, processed_nodes, "consider node {}".format(v))

            upper_indegree = get_upper_indegree(greedy_graph, v)
            upper_outdegree = get_upper_outdegree(greedy_graph, v)

            if upper_indegree > upper_outdegree:
                suff = v[1:] if v[1:] != "" else "eps"
                for _ in range(upper_indegree - upper_outdegree):
                    drawer.draw(greedy_graph, processed_nodes, "to balance {}, add edge {}->{}".format(v, v, suff))
                    greedy_graph.add_edge(v, suff)
                    drawer.draw(greedy_graph, processed_nodes)
                assert greedy_graph.in_degree(v) == greedy_graph.out_degree(v)
            elif upper_indegree < upper_outdegree:
                pref = v[:-1] if v[:-1] != "" else "eps"
                for _ in range(upper_outdegree - upper_indegree):
                    drawer.draw(greedy_graph, processed_nodes,
                                               "to balance {}, add edge {}->{}".format(v, pref, v))
                    greedy_graph.add_edge(pref, v)
                    drawer.draw(greedy_graph, processed_nodes)
                assert greedy_graph.in_degree(v) == greedy_graph.out_degree(v)
            else:
                assert upper_indegree == upper_outdegree

                # check whether we need to connect it to the rest of the graph
                sccs = nx.strongly_connected_components(greedy_graph)
                sccs = [C for C in sccs if v in C]
                assert len(sccs) == 1

                wccs = nx.weakly_connected_components(greedy_graph)
                wccs = [C for C in wccs if v in C]
                assert len(wccs) == 1

                scc = sccs[0]
                wcc = wccs[0]

                scc = sorted(scc)
                wcc = sorted(wcc)

                min_length_string_in_wcc = min(len(z) for z in wcc)

                #if not greedy_graph.has_node("eps") and scc == wcc and len(v) == min_length_string_in_wcc and sorted([u for u in scc if len(u) == len(v)])[-1] == v:
                if not "eps" in scc and scc == wcc and len(v) == min_length_string_in_wcc and sorted([u for u in scc if len(u) == len(v)])[-1] == v:
                    suff = v[1:] if v[1:] != "" else "eps"
                    pref = v[:-1] if v[:-1] != "" else "eps"

                    drawer.draw(greedy_graph, processed_nodes, "adding edges {}->{}->{} to connect the component to eps".format(pref, v, suff))

                    greedy_graph.add_edge(v, suff)
                    greedy_graph.add_edge(pref, v)
                    assert greedy_graph.in_degree(v) == greedy_graph.out_degree(v)

                    drawer.draw(greedy_graph, processed_nodes)
                else:
                    drawer.draw(greedy_graph, processed_nodes, "{} is balanced, skip it".format(v))

    drawer.draw(greedy_graph, processed_nodes, "Done!")
    drawer.draw(greedy_graph, processed_nodes, set_of_edges_to_superstring(greedy_graph))
    return list(zip(drawer.paths, drawer.descriptions))


construct_greedy_solution(["abc", "cba", "bca"])