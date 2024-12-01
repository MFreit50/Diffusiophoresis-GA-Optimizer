from interfaces.function import Function
from diffusiophoresis.variable import Variable
class x_squared(Function):

    def evaluate(self, equation):
        x = equation.get_value("x")
        return x**2
    
    def get_variables(self):
        return self.variables
    
    def _define_variables(self):
        self.variables = {
            "x": Variable(variable_name="x", value=1, is_constant=False, min_range=-10000, max_range=10000)
        }