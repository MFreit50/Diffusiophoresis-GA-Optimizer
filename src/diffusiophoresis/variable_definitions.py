import copy
from diffusiophoresis.variable import Variable
class VariableDefinitions():
    variables = {}

    @staticmethod
    def get_variables():
        return copy.deepcopy(VariableDefinitions.variables)

    def load_rastrigin():
        VariableDefinitions.variables = {
            "A": Variable(variable_name="A", value=10, is_constant=True, min_range=0, max_range=1000000),
            "X": Variable(variable_name="X", value=5000, is_constant=False, min_range=-5.12, max_range=5.12),
            "Y": Variable(variable_name="Y", value=5000, is_constant=False, min_range=-5.12, max_range=5.12),
            "n": Variable(variable_name="n", value=2, is_constant=True, min_range=0, max_range=1000000)
        }
    
    def load_diffusiophoresis():
        VariableDefinitions.variables = {
            "c_initial": Variable(variable_name="c_initial", value=0.0000001, is_constant=True, min_range=0, max_range=0),
            "diffusiophoretic_mobility": Variable(variable_name="diffusiophoretic_mobility", value=-3.1257057503129845e-12, is_constant=True, min_range=0, max_range=0),
            "channel_length":Variable(variable_name="channel_length", value=0, is_constant=False, min_range=0.0000001, max_range=10000),
            "channel_height":Variable(variable_name="channel_height", value=0, is_constant=False, min_range=0.0000001, max_range=10000),
            "channel_width":Variable(variable_name="channel_width", value=0, is_constant=False, min_range=0.0000001, max_range=10000),
            "fluid_velocity":Variable(variable_name="fluid_velocity", value=0, is_constant=False, min_range=0.0000001, max_range=100),
            "fluid_viscosity": Variable(variable_name="fluid_viscosity", value=0.1, is_constant=True, min_range=0.1, max_range=0.1),
            "dynamic_viscosity": Variable(variable_name="dynamic_viscosity", value=0.89, is_constant=True, min_range=0, max_range=0),
            "fluid_density":Variable(variable_name="fluid_density", value=1.0, is_constant=True, min_range=0, max_range=0)
        }