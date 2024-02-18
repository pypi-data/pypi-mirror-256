from ssim import grid

feeder_model = "ieee13nodeckt.dss"

# Need a datastructure that can specify how to construct a grid simulation.
# It must be serializable and passed to a new process where it is used to
# instantiate a grid model.
sim = simulator.Simulation(feeder_model)

grid_description = grid.Grid()

device_specs = {
    "phases": 3,
    "kV": 4.16,
    "pf": 1.0,
    "kwrated": 5000,
    "kwhrated": 50000,
    "%stored": 50,
    "state": "idling"
}

sim.add_storage(
    "Storage632", "632", device_specs,
    efficiency=
)