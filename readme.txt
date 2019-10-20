Run with Python 3.6+

Usage:
"python [script]" 

where script is out of the following three files:

TSP - mst.py
TSP - SAnn2.py
TSP - GA.py

representing the following methods:

Minimum Spanning Tree heuristic, using Christofides (should be max 1.5 times the optimal)
Simulated Annealing (gets rather close but never fully converges -- takes a long time)
Genetic Algorithm (might need more generations -- does not converge before reaching the max # generations)

Go into the files to change the "*.tsp" file to read from either

a280.tsp (symmetric graph)
eil51.tsp (especially used to test christofides)
test.tsp (first 10 samples of a280.tsp)

Tests have been mostly implemented for only the MST method.

Any other files can be download from the TSPLib site (along with the optimal routes/costs found).



Please also check TSP - SAnn (not the second) to see an unfinished manual implementation attempt. 

Also screw Christofides (2 NP-hard problems inside an NP-hard...)

