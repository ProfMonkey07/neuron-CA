# neuron-CA
a CA to model neurons<br>
The cellular automata has 4 types of cells, and each cell contains a charge as part of its state as well<br>
these types are void, dendrite, cell body, and axon<br>
at each time step, the hexagonal grid is updated based on the following rules:<br>
* at the start of a time step, if a cell body has a charge greater than the threshhold, its charge goes to 0<br>
* dendrites have a charge equal to the sum of the charges of neighboring axons<br>
* axons have a charge of 1 if a neighboring cell body has a charge above the threshhold<br>
* cell bodies gain charge equal to the sum of neighboring dendrite charges<br>
* void stays void
You will need to have pygame installed for this, you can use the number keys 0, 1, 2, and 3 to change cell states if you hover your mouse over the cell and press the key, you can also use q and w to increase or decrease the charge respectively, lighter cells mean higher charge, blue cells are axons, red are dendrites, green are cell bodies, and grey is void
