# Collapsing Superstring Conjecture

In this project we provide some tools to test the Collapsing Superstring Conjecture on various instances.

In order to run the python scripts you will need **graphviz** and **pygraphviz**. You can install them as follows: 

	brew install graphviz
    pip3 install pygraphviz

Now you are ready to run the main scripts. For example, you can run the following command:

	python3 code/hierarchical_graph.py
    
In the folder output/ you should see all steps of the Greedy Hierarchical Algorithm for the input string *ccabab*, *ababab*, *babacc*.