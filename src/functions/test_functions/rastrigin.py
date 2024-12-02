from functions.rastrigin import Rastrigin
from interfaces.test_function import TestFunction
class RastriginTest(Rastrigin, TestFunction):
    def solution(self):
        return [0,0]