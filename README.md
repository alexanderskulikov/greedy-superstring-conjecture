# Collapsing Superstring Conjecture

In this project we provide some tools to test the Collapsing Superstring Conjecture on various instances.

In order to run the python scripts you will need **graphviz** and **pygraphviz**. You can install them as follows: 

	brew install graphviz
    pip3 install pygraphviz

Now you are ready to run the main scripts. For example, you can run the following commands:

	cd code
    python3 
    from hierarchical_graph import * 
    construct_greedy_solution(["abba", "abca", "aac", "cab", "bab", "dbb"])
    
In the folder code/output you should see all steps of the Greedy Hierarchical Algorithm for the input string *abba*, *abca*, *aac*, *cab*, *bab*, *dbb*.


To run a web-interface, install flask and then, in the folder web:
    
    FLASK_APP=csc.py
    flask run
    
Then proceed to http://localhost:5000/scs


