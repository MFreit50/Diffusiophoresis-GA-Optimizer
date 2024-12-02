import math
from diffusiophoresis.variable import Variable
from interfaces.function import Function
class Rastrigin(Function):
    
    def evaluate(self, x, *args):
        x1 = x[0]
        x2 = x[1]
        #A, n = args
        A = 10
        n = 2
        return (A*n) + (x1**2 - A * math.cos(2*math.pi*x1)) + (x2**2 - A * math.cos(2*math.pi*x2))
    
    def get_parameters(self):
        func = self.evaluate
        bounds = [(-5.12, 5.12)]*2
        args = (10, 2)
        return (func, bounds, args)