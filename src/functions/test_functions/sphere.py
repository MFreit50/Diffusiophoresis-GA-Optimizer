from functions.sphere import Sphere
from interfaces.test_function import TestFunction
class SphereTest(Sphere, TestFunction):
    def solution(self):
        return [0,0]