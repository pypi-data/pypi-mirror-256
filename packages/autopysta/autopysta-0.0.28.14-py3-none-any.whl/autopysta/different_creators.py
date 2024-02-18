# ------------------------------------------------------------------------------
# Case of study: Different Creators
#
# In this example we use different creators that create vehicles with different
# models associated to them. The creators use are fixed_state_creator (that is 
# centered on using a given spacing and initial speed) and fixed_demand_creator
# (that is centered on using a given flow).
# ------------------------------------------------------------------------------

# Import the library
import autopysta as ap

# We define the geometry of the highway the simulation will use. It 
# takes as arguments the length of the highway, number of lanes, position where
# the merge ramp ends (0 for no merge ramp) and the position where the diverge
# ramp ends (length of the highway for no diverge ramp).
geo = ap.geometry(1000, 3, 300, 700)

# Define the acceleration/desacceleration models with default parameters the creators 
# are going to use.
idm = ap.idm()
gipps = ap.gipps()

# Next we define the types of creators each lane will use. The creators basically
# create vehicles when the necessary conditions (defined by each type of creator)
# are met. If only one is specified then all lanes will have that creator. The final 
# parameter is optional, it sets the number of vehicles to create (infinite by default).
ccrr=[
    ap.fixed_state_creator(gipps, 15, 10),
    ap.fixed_demand_creator(idm, 0.5),
    ap.fixed_state_creator(idm, 15, 10),
    ap.fixed_demand_creator(gipps, 0.5),
]

# One last setting to define is the lane-changing model. If the user don't want to
# allow lane changing then it can use the no_lch model.
lcm = ap.lcm_gipps()

# The simulation object is defined the previous settings to run for 80 seconds and
# with a deltaTime of 0.1 seconds. Because we don't want vehicles with given trajectories
# we just use an empty array.
s = ap.simulation(lcm, 80, geo, ccrr, [], 0.1)

# Finally, the simulation is run, where upon finishing it will will return a results
# object, that contains important data about the trajectories from the simulation.
r = s.run()

# The plot_x_vs_t method can be called to plot the trajectories of all lanes and 
# certain lanes
r.plot_x_vs_t()     # Plot all lanes
r.plot_x_vs_t(1)    # Plot lane 1
r.plot_x_vs_t(2)    # Plot lane 2
r.plot_x_vs_t(3)    # Plot lane 3
r.plot_x_vs_t(4)    # Plot lane 4