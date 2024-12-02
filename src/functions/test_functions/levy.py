from functions.levy import Levy
from interfaces.test_function import TestFunction
class LevyTest(Levy, TestFunction):
    def solution(self):
        return [1,1]