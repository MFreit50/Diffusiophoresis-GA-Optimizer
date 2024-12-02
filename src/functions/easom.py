from interfaces.function import Function
from diffusiophoresis.variable import Variable
import math
class Easom(Function):

    def evaluate(self,x ,*args):
        x1 = x[0]
        x2 = x[1]
        return -math.cos(x1) * math.cos(x2) * math.exp(-((x1 - math.pi)**2) - ((x2 - math.pi)**2))
    
    def get_parameters(self):
        func = self.evaluate
        bounds = [(-100, 100)]*2
        args = None
        return (func, bounds, args)