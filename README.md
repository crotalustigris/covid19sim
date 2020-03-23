# covid19sim
A simple Python simulator for covid19 (or other epidemics)

The simulator is documented in the code. It uses the SEIR epidemic model approach, but uses discrete time steps and calculations, 
rather than calculus. This makes it easier to understand and allows print statements to be used for debugging in a more intuitive way.

It also allows interventions to be put in a specific times which change the reproduction rate R from the basic reproduction rate R0.
