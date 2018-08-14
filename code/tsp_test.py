import tsp
import unittest
import networkx as nx
import math
from itertools import permutations


class TestTSP(unittest.TestCase):
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

    def dist(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def path_length(self, g, path):
        assert len(path) == g.number_of_nodes()
        return sum(g[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))

    def read_graph(self, test_index):
        g = nx.DiGraph()
        coors = self.coordinates[test_index]
        n = len(coors)
        for i in range(n):
            for j in range(n):
                g.add_edge(i, j, weight=self.dist(coors[i][0], coors[i][1], coors[j][0], coors[j][1]))
        return g

    def trivial_solution(self, g, begin):
        # n is the number of vertices.
        n = g.number_of_nodes()

        # Iterate through all permutations of n vertices with a fixed start vertex
        all = [i for i in range(n) if i != begin]
        opt = float('inf')
        for p in permutations(all):
            # Write your code here.
            opt = min(opt, self.path_length(g, (begin,) + p))

        return opt

    def test(self):
        for test_index in range(len(self.coordinates) - 2):
            n = len(self.coordinates[test_index])
            begin = n // 2
            g = self.read_graph(test_index)
            correct_result = self.trivial_solution(g, begin)
            result, path = tsp.dynamic_programming(g, begin)
            computed_result = self.path_length(g, path)
            self.assertLessEqual(math.fabs(result - computed_result), 0.001)
            self.assertLessEqual(math.fabs(result - correct_result), 0.001)


if __name__ == '__main__':
    unittest.main()
