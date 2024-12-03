import numpy as np
from interfaces.function import Function
from diffusiophoresis.variable import Variable
import math

class Levy(Function):

    def evaluate(self, x, *args):
        x1 = x[0]
        x2 = x[1]
        w1 = 1 + (x1 - 1) / 4
        w2 = 1 + (x2 - 1) / 4
        term1 = np.sin(np.pi * w1) ** 2
        term2 = (w1 - 1) ** 2 * (1 + 10 * np.sin(np.pi * w2) ** 2)
        term3 = (w2 - 1) ** 2 * (1 + np.sin(2 * np.pi * w2) ** 2)
        return term1 + term2 + term3

    def get_parameters(self):
        func = self.evaluate
        bounds = [(-10,10)]*2
        args = None
        return (func, bounds, args)
