from abc import ABC, abstractmethod

class Function(ABC):
    @abstractmethod
    def evaluate(self, x, *args):
        pass

    @abstractmethod
    def get_parameters(self):
        pass