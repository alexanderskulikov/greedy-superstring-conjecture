import os
import pygraphviz as pgv
import shutil


class GraphDrawer:
    def __init__(self, strings, output_dir, print_description, disable=False):
        self.__prepare_hierarchical_graph__(strings)

        self.__disable__ = disable
        if self.__disable__:
            return

        self.__prepare_for_drawing__(output_dir, print_description)

    def __prepare_for_drawing__(self, output_dir, print_description):
        self.print_description = print_description
        self.output_dir = output_dir

        self.descriptions = []
        self.paths = []
        self.__file_number__ = 1

        self.create_output_folders()

    def __prepare_hierarchical_graph__(self, strings):
        assert len(strings)
        self.strings = list(strings)
        self.__empty_string_name__ = "eps"
        assert all(s != self.__empty_string_name__ for s in strings)

        self.HG = pgv.AGraph(strict=False, directed=True)
        self.HG.add_node(self.__empty_string_name__)

        # set up layers
        max_length = max(len(s) for s in self.strings)

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
            if node != self.__empty_string_name__:
                pref = node[:-1] if len(node) > 1 else self.__empty_string_name__
                suf = node[1:] if len(node) > 1 else self.__empty_string_name__
                self.HG.add_edge(pref, node, constraint='false')
                self.HG.add_edge(node, suf, constraint='true')

        # stick nodes to appropriate layers
        for layer in range(max_length + 1):
            sub_graph = self.HG.add_subgraph(fixed_length_strings[layer], name="s"+str(layer))
            if layer == 0:
                sub_graph.graph_attr['rank'] = 'sink'
            elif layer == max_length:
                sub_graph.graph_attr['rank'] = 'source'
            else:
                sub_graph.graph_attr['rank'] = 'same'

        self.__set_default_attributes__()

        # highlight input strings
        for string in strings:
            self.HG.get_node(string).attr['shape'] = 'rectangle'
            self.HG.get_node(string).attr['style'] = 'filled'
            self.HG.get_node(string).attr['fillcolor'] = 'white'

        # self.HG.

        self.HG.layout(prog='dot')

    def create_output_folders(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        else:
            shutil.rmtree(self.output_dir)
            os.makedirs(self.output_dir)

    def __set_default_attributes__(self):
        for (u, v) in self.HG.edges():
            self.HG.get_edge(u, v).attr['color'] = "grey"
            self.HG.get_edge(u, v).attr['penwidth'] = 2

        for v in self.HG.nodes():
            self.HG.get_node(v).attr['style'] = 'filled'
            self.HG.get_node(v).attr['fillcolor'] = 'white'
            self.HG.get_node(v).attr['penwidth'] = 2

    def clear(self):
        if self.__disable__:
            return

        self.paths.clear()
        self.descriptions.clear()
        self.__file_number__ = 1

    def set_output_folder(self, output_folder):
        self.output_dir = output_folder
        self.create_output_folders()

    def draw(self, solution_edges, highlighted_nodes=None, description=" ", color="red", highlighted_edges=None):
        if self.__disable__:
            return 

        edges = list(solution_edges.edges())
        if highlighted_edges:
            for (u, v) in highlighted_edges:
                edges.remove((u, v))

        for (u, v) in edges:
            self.HG.get_edge(u, v).attr['color'] += ":" + color
            # self.HG.get_edge(u, v).attr['penwidth'] = 1

        if highlighted_edges:
            for (u, v) in highlighted_edges:
                self.HG.get_edge(u, v).attr['color'] += ":" + "green"

        if highlighted_nodes:
            for v in highlighted_nodes:
                assert self.HG.has_node(v)
                self.HG.get_node(v).attr['style'] = 'filled'
                self.HG.get_node(v).attr['fillcolor'] = color

        output_path = "{}/{}{}.jpg".format(self.output_dir,
                                           "0" * (3 - len(str(self.__file_number__))), self.__file_number__)
        self.HG.draw(output_path)
        self.__file_number__ += 1
        self.descriptions.append(description)
        self.paths.append(output_path)

        self.__set_default_attributes__()
