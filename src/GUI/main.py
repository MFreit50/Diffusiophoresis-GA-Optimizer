from main_application import MainApplication
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from diffusiophoresis.variable import Variable
from Modules.data_engine import DataEngine
from Modules.main_coordinator import MainCoordinator

if __name__ == "__main__":
    main_coordinator = MainCoordinator()
    main_coordinator.initialize()


def initialize_variables():
    variable_names = [
        "absolute_temperature",
        "channel_length",
        "channel_height",
        "fluid_density",
        "fluid_viscosity",
        "fluid_velocity",
        "beta_potential",
    ]

    variables = []
    
    # Initialize all variables with value=0, is_constant=False, min_range=0, max_range=1000
    for name in variable_names:
        variable = Variable(name, 0.0, False, 0.0, 0.0)
        variables.append(variable)
    
    # Write variable list using DataEngine
    data_engine = DataEngine()
    print(variable_names)
    
    for var in variables:
        print(f"{var} is of type {type(var)}")

    data_engine.write_variable_list(variables)