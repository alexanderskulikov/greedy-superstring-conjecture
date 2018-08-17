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


def construct_greedy_solution(strings, print_description=True, output_folder='output'):
    drawer = graph_drawer.GraphDrawer(strings)
    drawer.set_print_description(print_description)
    drawer.set_output_dir(output_folder)
    drawer.draw("initial hierarchical graph")
    drawer.draw("we first process input strings")

    greedy_graph = nx.MultiDiGraph()

    for s in sorted(strings):
        pref = s[:-1] if s[:-1] != "" else "eps"
        suff = s[1:]  if s[1:]  != "" else "eps"

        drawer.draw(
            description="{} is an input string hence we add two bottom edges to it: {}->{}->{}".format(s, pref, s, suff),
            highlighted_node=s
        )

        greedy_graph.add_edge(pref, s)
        greedy_graph.add_edge(s, suff)

        drawer.highlight_edge(pref, s)
        drawer.highlight_edge(s, suff)
        drawer.draw()

    drawer.draw("we now process nodes from top to bottom in lexicographical ordering")

    max_level = max(len(s) for s in strings)
    cur_level = max_level - 1

    while not greedy_graph.has_node("eps"):
        #assert cur_level > 0
        cur_level_vertices = sorted([v for v in greedy_graph.nodes() if len(v) == cur_level])
        cur_level -= 1

        for v in cur_level_vertices:
            drawer.draw(description="consider node {}".format(v), highlighted_node=v)

            upper_indegree = get_upper_indegree(greedy_graph, v)
            upper_outdegree = get_upper_outdegree(greedy_graph, v)

            if upper_indegree > upper_outdegree:
                suff = v[1:] if v[1:] != "" else "eps"
                for _ in range(upper_indegree - upper_outdegree):
                    drawer.draw("to balance {}, add edge {}->{}".format(v, v, suff))
                    greedy_graph.add_edge(v, suff)
                    drawer.highlight_edge(v, suff)
                    drawer.draw()
                assert greedy_graph.in_degree(v) == greedy_graph.out_degree(v)
            elif upper_indegree < upper_outdegree:
                pref = v[:-1] if v[:-1] != "" else "eps"
                for _ in range(upper_outdegree - upper_indegree):
                    drawer.draw("to balance {}, add edge {}->{}".format(v, pref, v))
                    greedy_graph.add_edge(pref, v)
                    drawer.highlight_edge(pref, v)
                    drawer.draw()
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

                    drawer.draw("adding edges {}->{}->{} to connect the component to eps".format(pref, v, suff))

                    greedy_graph.add_edge(v, suff)
                    greedy_graph.add_edge(pref, v)
                    assert greedy_graph.in_degree(v) == greedy_graph.out_degree(v)
                    drawer.highlight_edge(v, suff)
                    drawer.highlight_edge(pref, v)

                    drawer.draw()
                else:
                    drawer.draw("{} is balanced, skip it".format(v))

    drawer.draw("Done!")
    drawer.draw_solution()
    return list(zip(drawer.paths, drawer.descriptions))


