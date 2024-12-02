from interfaces.function import Function
from diffusiophoresis.diffusiophoresis_formulas import DiffusiophoresisFormulas
class Diffusiophoresis(Function):
    
    def evaluate(self, x):
        channel_height = x[0]
        channel_length = x[1]
        channel_width = x[2]
        mean_flow_velocity = x[3]

        c_initial = 0.0000001
        diffusiophoretic_mobility = -3.1257057503129845e-12
        chemiphoretic_gradient = DiffusiophoresisFormulas.chemiphoretic_gradient(c_initial, channel_height)
        diffusiophoretic_velocity = DiffusiophoresisFormulas.diffusiophoretic_velocity(diffusiophoretic_mobility, chemiphoretic_gradient)
        return DiffusiophoresisFormulas.exclusion_zone_area(channel_height, channel_length, channel_width, mean_flow_velocity, diffusiophoretic_velocity)

    def get_parameters(self):
        func = self.evaluate
        bounds = [(0.0000001, 10000)]*4
        args = None
        return (func, bounds, args)
    
    '''
    def _define_variables(self):
        self.variables = {
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
    '''