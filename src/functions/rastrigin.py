import math
from diffusiophoresis.variable import Variable
from interfaces.function import Function
class Rastrigin(Function):
    
    def evaluate(self, equation):
        A = equation.get_value("A")
        n = equation.get_value("n")
        x = equation.get_value("x")
        y = equation.get_value("y")
        return self.evaluate_coordinates(x, y, A, n)

    def evaluate_coordinates(self, *args):
        x, y, A, n = args
        return (A*n) + (x**2 - A * math.cos(2*math.pi*x)) + (y**2 - A * math.cos(2*math.pi*y))
    
    def get_variables(self):
        return self.variables
    
    def _define_variables(self):
        self.variables = {
            "A": Variable(variable_name="A", value=10, is_constant=True, min_range=0, max_range=1000000),
            "x": Variable(variable_name="x", value=1, is_constant=False, min_range=-5.12, max_range=5.12),
            "y": Variable(variable_name="y", value=1, is_constant=False, min_range=-5.12, max_range=5.12),
            "n": Variable(variable_name="n", value=2, is_constant=True, min_range=0, max_range=1000000)
        }