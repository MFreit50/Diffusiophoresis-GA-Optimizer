import math
from functions.easom import Easom
from interfaces.test_function import TestFunction
class EasomTest(Easom, TestFunction):
    def solution(self):
        return [math.pi,math.pi]