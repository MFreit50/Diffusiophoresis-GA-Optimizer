from interfaces.function import Function
from diffusiophoresis.variable import Variable
import math

class Ackley(Function):

    def evaluate(self, x, *args):
        x1 = x[0]
        x2 = x[1]
        term1 = -20 * math.exp( -0.2 * math.sqrt( 0.5 * ((x1**2) + (x2**2)) ))
        term2 = - math.exp( 0.5 * (math.cos(2*math.pi*x1) + math.cos(2*math.pi*x2)) )
        return term1 + term2 + math.e + 20
    
    def get_parameters(self):
        func = self.evaluate
        bounds = [(-5.12,5.12)]*2
        args = None
        return (func, bounds, args)