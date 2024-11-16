import numpy as np
from interfaces.function import Function
from diffusiophoresis.variable import Variable
import math

class Levy(Function):

    def evaluate(self, equation):
        x = equation.get_value("x")
        y = equation.get_value("y")
        return self.evaluate_coordinates(x, y)

    def evaluate_coordinates(self, *args):
        x, y = args
        w1 = 1 + (x + 1) / 4
        w2 = 1 + (y + 1) / 4
        term1 = np.sin(np.pi * w1) ** 2
        term2 = (w2 - 1) ** 2 * (1 + 10 * np.sin(np.pi * w2 + 1) ** 2)
        term3 = (w2 - 1) ** 2 * (1 + np.sin(2 * math.pi * w2) ** 2)
        return term1 + term2 + term3

    def get_variables(self):
        return self.variables
    
    def get_domain(self):
        return (-10, 10), (-10, 10)
    
    def _define_variables(self):
        self.variables = {
            "x": Variable(variable_name="x", value=1, is_constant=False, min_range=-10, max_range=10),
            "y": Variable(variable_name="y", value=1, is_constant=False, min_range=-10, max_range=10)
        }