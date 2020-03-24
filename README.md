# covid19sim
A simple Python simulator for covid19 (or other epidemics)

The simulator is documented in the code. It uses the SEIR epidemic model approach, but uses discrete time steps and calculations, 
rather than calculus. This makes it easier to understand and allows print statements to be used for debugging in a more intuitive way.

It also allows interventions to be put in a specific times which change the reproduction rate R from the basic reproduction rate R0.

IT IS IMPORTANT TO KNOW THAT I am NOT a professional in the field. DO NOT use the numbers from this as meaningful in any predictive sense. It is a little tool for one to get a feel for how an epidemic behaves. It is a very simple model - there is no attempt to make this precise. The few parameters it has are not the final word. For example, it treats all cases has having the same parameters: incubaiton period (latency) and infectious period. This is not realistic. It treats every day of the infectious period as having the same infectivity. Again, not realistic.
