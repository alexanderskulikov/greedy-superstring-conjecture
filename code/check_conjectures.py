import hierarchical_graph
import graph_drawer
import networkx as nx
from exact_solution import shortest_superstring


def compare_graphs(g, h):
    return nx.difference(g, h).number_of_edges() == 0 and \
           nx.difference(h, g).number_of_edges() == 0


def log(input_strings, exact_sol, hier_sol):
    return "%s\nExact Solution has length %d:\n%s\nGreedy Hierarchical Solution has length %d:\n%s\n\n"\
           % (input_strings, len(exact_sol), exact_sol, len(hier_sol), hier_sol)


def log_counter_example(log_file, input_strings, exact_sol, hier_sol, description):
    with open(log_file, 'a+') as output_file:
        output_file.write(description+'\n')
        output_file.write(log(input_strings, exact_sol, hier_sol))



def log_counter_examples(log_file, input_strings, exact_sol, hier_sol, hier_graph, exact_graph, trivial_graph):
    if len(hier_sol) >= 2 * len(exact_sol):
        log_counter_example(log_file, input_strings, exact_sol, hier_sol,
                            'The Greedy Hierarchical solution is twice longer than the optimal one')
    if not compare_graphs(hier_graph, exact_graph):
        log_counter_example(log_file, input_strings, exact_sol, hier_sol,
                            'The Greedy Hierarchical solution does not equal the collapsed exact solution')
    if not compare_graphs(hier_graph, trivial_graph):
        log_counter_example(log_file, input_strings, exact_sol, hier_sol,
                            'The Greedy Hierarchical solution does not equal the collapsed trivial solution')


def check(log_file, strings):
    drawer = graph_drawer.GraphDrawer(strings, 'output', False, True)
    hier_sol, hier_graph = hierarchical_graph.construct_greedy_solution(strings, drawer)

    opt_permutation = shortest_superstring(strings)
    opt_strings = [strings[i] for i in opt_permutation]
    exact_sol, exact_graph = hierarchical_graph.collapse_for_permutation(opt_strings, drawer)

    trivial_sol, trivial_graph = hierarchical_graph.collapse_for_permutation(strings, drawer)

    log_counter_examples(log_file, strings, exact_sol, hier_sol, hier_graph, exact_graph, trivial_graph)


def check_dataset(log_file, dataset_file='../web/static/datasets.txt'):
    with open(dataset_file, 'r') as presets_file:
        presets = presets_file.readlines()
        presets = [x.strip() for x in presets]
        for preset in presets:
            check(log_file, preset.split(' '))


# check_dataset('counter-examples.txt')