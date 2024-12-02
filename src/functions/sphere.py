from interfaces.function import Function
from diffusiophoresis.variable import Variable
class Sphere(Function):

    def evaluate(self, x, *args):
        x1 = x[0]
        x2 = x[1]
        return x1**2 + x2**2
    
    def get_parameters(self):
        func = self.evaluate
        bounds = [(-5.12,5.12)]*2
        args = None
        return (func, bounds, args)