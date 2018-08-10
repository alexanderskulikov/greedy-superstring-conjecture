from flask import Flask
from flask import render_template
from ..code import hierarchical_graph
#from ..code.graph_drawer import *
#from ..code.hierarchical_graph import *

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    # hier = [('static/output/001.png', 'a'), ('static/output/002.png', 'b'),('static/output/003.png', 'c'), ('static/output/004.png', 'd'), ('static/output/005.png', 'e'), ('static/output/006.png', 'f'), ]
    hier = hierarchical_graph.construct_greedy_solution(["ccabab", "ababab", "babacc"], False, 'static/output')
    # hier = hierarchical_graph.construct_greedy_solution(["a", "b", "c"], False, 'static/output')
    exact = hier
    trivial = hier
    return render_template('index.html', hier=hier, exact=exact, trivial=trivial)
