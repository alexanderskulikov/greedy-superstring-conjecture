import os
import pygraphviz as pgv
import shutil
import networkx as nx


class GraphDrawer:
    def __init__(self, strings, output_dir, print_description):
        self.__file_number__ = 1

        self.print_description = print_description
        self.output_dir = output_dir
        self.create_output_folders()

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
            if node != self.__empty_string_name__:# and not (node.isdigit()):
                pref = node[:-1] if len(node) > 1 else self.__empty_string_name__
                suf = node[1:] if len(node) > 1 else self.__empty_string_name__
                self.HG.add_edge(pref, node, constraint='false')
                self.HG.add_edge(node, suf, constraint='true')

        self.set_default_attributes()

        # highlight input strings
        for string in strings:
            self.HG.get_node(string).attr['shape'] = 'rectangle'
            self.HG.get_node(string).attr['style'] = 'filled'
            self.HG.get_node(string).attr['fillcolor'] = 'white'

        # add placeholder for description text
        # self.__description_node__ = "description"
        # fixed_length_strings[0].append(self.__description_node__)
        # self.HG.add_node(self.__description_node__)
        # self.HG.get_node(self.__description_node__).attr['color'] = 'white'
        # self.HG.get_node(self.__description_node__).attr['shape'] = 'rectangle'
        # self.HG.get_node(self.__description_node__).attr['width'] = 8
        # self.HG.get_node(self.__description_node__).attr['label'] = ''

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

    def create_output_folders(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        else:
            shutil.rmtree(self.output_dir)
            os.makedirs(self.output_dir)

    def set_default_attributes(self):
        for (u, v) in self.HG.edges():
            self.HG.get_edge(u, v).attr['color'] = "grey"
            self.HG.get_edge(u, v).attr['penwidth'] = 1

        for v in self.HG.nodes():
            self.HG.get_node(v).attr['style'] = 'filled'
            self.HG.get_node(v).attr['fillcolor'] = 'white'

    def draw(self, solution_edges, highlighted_nodes=None, description=" ", color="turquoise"):
        for (u, v) in solution_edges.edges():
            self.HG.get_edge(u, v).attr['color'] += ":" + color
            self.HG.get_edge(u, v).attr['penwidth'] = 2

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

        self.set_default_attributes()



