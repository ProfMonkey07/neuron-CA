# neuron-CA
a CA to model neurons
The cellular automata has 4 types of cells, and each cell contains a charge as part of its state as well
these types are void, dendrite, cell body, and axon
at each time step, the hexagonal grid is updated based on the following rules:
at the start of a time step, if a cell body has a charge greater than the threshhold, its charge goes to 0
dendrites have a charge equal to the sum of the charges of neighboring axons
axons have a charge of 1 if a neighboring cell body has a charge above the threshhold
cell bodies gain charge equal to the sum of neighboring dendrite charges
void stays void
