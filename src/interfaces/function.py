from abc import ABC, abstractmethod

import math
class Function(ABC):
    def __init__(self):
        self.variables = {}
        self._define_variables()

    @abstractmethod
    def evaluate(self, equation):
        pass
    
    def evaluate_coordinates(self, *args):
        pass

    @abstractmethod
    def get_variables(self):
        pass
    
    @abstractmethod
    def get_domain(self):
        pass

    @abstractmethod
    def _define_variables(self):
        pass