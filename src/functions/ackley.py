from interfaces.function import Function
from diffusiophoresis.variable import Variable
import math

class Ackley(Function):

    def evaluate(self, equation):
        x = equation.get_value("x")
        y = equation.get_value("y")
        return self.evaluate_coordinates(x,y)
    
    def evaluate_coordinates(self, *args):
        x, y = args
        term1 = -20 * math.exp( -0.2 * math.sqrt( 0.5 * ((x**2) + (y**2)) ))
        term2 = - math.exp( 0.5 * (math.cos(2*math.pi*x) + math.cos(2*math.pi*y)) )
        return term1 + term2 + math.e + 20
    
    def get_variables(self):
        return self.variables
    
    def _define_variables(self):
        self.variables = {
            "x": Variable(variable_name="x", value=1, is_constant=False, min_range=-5.12, max_range=5.12),
            "y": Variable(variable_name="y", value=1, is_constant=False, min_range=-5.12, max_range=5.12)
        }