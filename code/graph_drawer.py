import os
import pygraphviz as pgv
import shutil
import copy

class GraphDrawer:
    def __init__(self, strings):
        self.__file_number__ = 1

        self.print_description = True
        self.output_folder = 'output'

        assert len(strings)
        self.strings = list(strings)
        self.__empty_string_name__ = "eps"
        assert all(s != self.__empty_string_name__ for s in strings)
        self.descriptions = []
        self.paths = []

        self.HG = pgv.AGraph(strict=False, directed=True)
        self.HG.add_node(self.__empty_string_name__)

        # set up layers
        max_length = max(len(s) for s in self.strings)
        # for layer in range(max_length):
        #     self.HG.add_edge(layer + 1, layer, constraint='true', color='white')
        # for layer in range(max_length + 1):
        #     self.HG.get_node(layer).attr['color'] = 'white'
        #     self.HG.get_node(layer).attr['fontcolor'] = 'white'
        # self.HG.add_edge(0, max_length, constraint='false', color='white')

        # populating the graph
        fixed_length_strings = [[str(i)] for i in range(max_length + 1)]
        fixed_length_strings[0].append(self.__empty_string_name__)

        for string in strings:
            for i in range(len(string)):
                for j in range(i + 1, len(string) + 1):
                    substring = string[i:j]
                    assert len(substring)
                    if not self.HG.has_node(substring):
                        self.HG.add_node(substring)
                        fixed_length_strings[len(substring)].append(substring)

        for node in self.HG.nodes():
            if node != self.__empty_string_name__ and not (node.isdigit()):
                pref = node[:-1] if len(node) > 1 else self.__empty_string_name__
                suf = node[1:] if len(node) > 1 else self.__empty_string_name__
                self.HG.add_edge(pref, node, constraint='false', color='grey')
                self.HG.add_edge(node, suf, constraint='true', color='grey')

        # highlight input strings
        for string in strings:
            self.HG.get_node(string).attr['shape'] = 'rectangle'
            self.HG.get_node(string).attr['style'] = 'filled'
            self.HG.get_node(string).attr['fillcolor'] = 'white'

        # add placeholder for description text
        self.__description_node__ = "description"
        fixed_length_strings[0].append(self.__description_node__)
        self.HG.add_node(self.__description_node__)
        self.HG.get_node(self.__description_node__).attr['color'] = 'white'
        self.HG.get_node(self.__description_node__).attr['shape'] = 'rectangle'
        self.HG.get_node(self.__description_node__).attr['width'] = 8
        self.HG.get_node(self.__description_node__).attr['label'] = ''

        # stick nodes to appropriate layers
        for layer in range(max_length + 1):
            sub_graph = self.HG.add_subgraph(fixed_length_strings[layer], name="s"+str(layer))
            if layer == 0:
                sub_graph.graph_attr['rank'] = 'sink'
            elif layer == max_length:
                sub_graph.graph_attr['rank'] = 'source'
            else:
                sub_graph.graph_attr['rank'] = 'same'

        self.HG.layout(prog='dot')

        self.__output_dir__ = "output"
        if not os.path.exists(self.__output_dir__):
            os.makedirs(self.__output_dir__)
        else:
            shutil.rmtree(self.__output_dir__)
            os.makedirs(self.__output_dir__)

    def draw(self, description=" ", highlighted_node=None):
        if highlighted_node:
            assert self.HG.has_node(highlighted_node)
            self.HG.get_node(highlighted_node).attr['style'] = 'filled'
            self.HG.get_node(highlighted_node).attr['fillcolor'] = 'turquoise'

        if self.print_description:
            self.HG.get_node(self.__description_node__).attr['label'] = description
        elif self.HG.has_node(self.__description_node__):
            self.HG.remove_node(self.__description_node__)

        output_path = "{}/{}{}.jpg".format(self.output_folder, "0" * (3 - len(str(self.__file_number__))), self.__file_number__)
        self.HG.draw(output_path)
        self.__file_number__ += 1
        self.descriptions.append(description)
        self.paths.append(output_path)

        # if highlighted_node:
        #     self.HG.get_node(highlighted_node).attr['fillcolor'] = 'white'

    def euler_cycle(self, graph, cycle, node='eps'):
        neighbors = graph.neighbors(node)
        for neighbor in graph.nodes():
            if graph.has_edge(node, neighbor):
                # graph.remove_edge removes one copy of the arc
                graph.remove_edge(node, neighbor)
                self.euler_cycle(graph, cycle, neighbor)
        cycle.append(node)

    def highlight_edge(self, from_node, to_node, color="turquoise"):
        assert self.HG.has_node(from_node)
        assert self.HG.has_node(to_node)
        self.HG.get_edge(from_node, to_node).attr['color'] += ":" + color

    def set_print_description(self, print_description):
        self.print_description = print_description

    def set_output_folder(self, output_folder):
        self.output_folder = output_folder

    def get_solution(self):
        result = ''
        graph = pgv.AGraph(strict=False, directed=True)
        for edge in self.HG.edges():
            if edge.attr['color'] == "grey:turquoise":
                graph.add_edge(edge)

        cycle = []
        self.euler_cycle(graph, cycle)
        result = ''
        for i in range(len(cycle)-1):
            cur = cycle[i]
            next = cycle[i + 1]
            if next != 'eps' and (cur == 'eps' or len(next) > len(cur)):
                result += next[0]
        return result

    def draw_solution(self):
        output_path = "{}/{}{}.jpg".format(self.output_folder, "0" * (3 - len(str(0))), 0)
        description = self.get_solution()
        if self.print_description:
            self.HG.get_node(self.__description_node__).attr['label'] = description
        self.HG.draw(output_path)
        self.descriptions.insert(0, description)
        self.paths.insert(0, output_path)
