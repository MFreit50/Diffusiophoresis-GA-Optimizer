from abc import ABC, abstractmethod
class Individual(ABC):
    @abstractmethod

    def optimize(self):
        pass

    def initialize(self):
        pass

    def randomize(self):
        pass