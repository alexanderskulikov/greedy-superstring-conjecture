# Collapsing Superstring Conjecture

In this project we provide some tools to test the Collapsing Superstring Conjecture on various instances.

In order to find an optimal solution to the Shortest Common Superstring problem (SCS), we use the [**Concorde** Traveling Salesman Solver](http://www.math.uwaterloo.ca/tsp/concorde.html).


## How to install Concorde on a Linux Machine

First we download the [**QSopt** Linear Programming Solver](https://www.math.uwaterloo.ca/~bico/qsopt/).

	mkdir qsopt
    cd qsopt
    wget http://www.math.uwaterloo.ca/~bico//qsopt/beta/codes/linux64/qsopt{.h,.a,}
    QSOPT_PATH=$PWD;
    
Now we're ready to download and install **Concorde**.

	cd ..
    wget http://www.math.uwaterloo.ca/tsp/concorde/downloads/codes/src/co031219.tgz
    tar xf co031219.tgz
    cd concorde
    ./configure --with-qsopt=$QSOPT_PATH
    make

In order to test the solver, we can run the following commands.

	cd TSP
    wget https://wwwproxy.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/tsp/a280.tsp.gz
    gunzip a280.tsp.gz
    ./concorde a280.tsp