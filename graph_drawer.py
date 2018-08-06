import pygraphviz as pgv


class GraphDrawer:
    def __init__(self, strings):
        assert len(strings)
        self.strings = list(strings)
        self.__empty_string_name__ = "eps"
        assert all(s != self.__empty_string_name__ for s in strings)

        self.HG = pgv.AGraph(strict=False, directed=True)
        self.HG.add_node(self.__empty_string_name__)

        # set up layers
        max_length = max(len(s) for s in self.strings)
        for layer in range(max_length):
            self.HG.add_edge(layer + 1, layer, constraint='true', color='white')
        for layer in range(max_length + 1):
            self.HG.get_node(layer).attr['color'] = 'white'
            self.HG.get_node(layer).attr['fontcolor'] = 'white'
        self.HG.add_edge(0, max_length, constraint='false', color='white')

        # populating the graph
        fixed_length_strings = [[str(i)] for i in range(max_length + 1)]
        fixed_length_strings[0].append(self.__empty_string_name__)

        for string in strings:
            fixed_length_strings[len(string)].append(string)

            for pref_length in range(len(string)):
                pref = string[:pref_length]
                if pref != "":
                    fixed_length_strings[len(pref)].append(pref)
                else:
                    pref = self.__empty_string_name__
                next_pref = string[:pref_length + 1]
                self.HG.add_edge(pref, next_pref, constraint='false')

            for suf_length in range(len(string)):
                suf = string[suf_length:]
                next_suf = string[suf_length + 1:]
                if next_suf != "":
                    fixed_length_strings[len(next_suf)].append(next_suf)
                else:
                    next_suf = self.__empty_string_name__
                self.HG.add_edge(suf, next_suf, constraint='true')

        # highlight input strings
        for string in strings:
            self.HG.get_node(string).attr['shape'] = 'rectangle'
            self.HG.get_node(string).attr['style'] = 'filled'
            self.HG.get_node(string).attr['fillcolor'] = 'red'

        # stick nodes to appropriate layers
        for layer in range(max_length + 1):
            sub_graph = self.HG.add_subgraph(fixed_length_strings[layer], name="s"+str(layer))
            if layer == 0:
                sub_graph.graph_attr['rank'] = 'sink'
            elif layer == max_length:
                sub_graph.graph_attr['rank'] = 'source'
            else:
                sub_graph.graph_attr['rank'] = 'same'

    def __get_node_name__(self, node_name):
        return node_name if node_name != "" else self.__empty_string_name__

    def draw(self, file_name, description=None):
        assert description != ""

        text = description if description else "" * 30
        self.HG.add_node(text)

        self.HG.get_node(text).attr['color'] = 'white'
        if not description:
            self.HG.get_node(text).attr['fontcolor'] = 'white'

        sub_graph = self.HG.add_subgraph([self.__empty_string_name__, description], name="description")
        sub_graph.graph_attr['rank'] = 'same'

        self.HG.layout(prog='dot')
        self.HG.draw("{}.png".format(file_name))

gd = GraphDrawer(["ab", "ba"])
gd.draw(file_name="output", description="This is hierarchical graph")


gd = GraphDrawer(["abc", "bac", "cab"])
gd.draw(file_name="output2", description="Another one")