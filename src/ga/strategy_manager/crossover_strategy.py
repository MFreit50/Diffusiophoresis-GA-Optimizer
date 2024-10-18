from abc import ABC, abstractmethod
import numpy as np
import random # TODO Remove this import and use numpy instead
from diffusiophoresis.equation import Equation

class CrossoverStrategy(ABC):
    @abstractmethod
    def crossover(self, crossover_rate: float, parent1: Equation, parent2: Equation) -> tuple[Equation, Equation]:
        pass

class UniformCrossover(CrossoverStrategy):
    def crossover(self, crossover_rate: float, parent1: Equation, parent2: Equation) -> tuple[Equation, Equation]:

        if np.random.rand() > crossover_rate:
            return parent1, parent2

        parent1_vars = parent1.get_variable_list()
        parent2_vars = parent2.get_variable_list()

        # TODO: Debug: Check if both parents have the same variables for crossover

        child1 = Equation()
        child2 = Equation()

        for i in range(len(parent1_vars)):
            if np.random.rand() < 0.5:
                child1.add_variable(parent1_vars[i])
                child2.add_variable(parent2_vars[i])
            else:
                child1.add_variable(parent2_vars[i])
                child2.add_variable(parent1_vars[i])

        return child1, child2

class SinglePointCrossover(CrossoverStrategy):
    def crossover(self, crossover_rate: float, parent1 : Equation, parent2 : Equation) -> tuple[Equation, Equation]:

        if np.random.rand() > crossover_rate:
            return parent1, parent2

        #aquire 1 variable from each parent
        variable_1 = random.choice(parent1.get_variable_list(filter_constants=True))
        variable_2 = random.choice(parent2.get_variable_list(filter_constants=True))

        #switch the variable between parents to create child
        child1 = parent1
        child2 = parent2

        child1.add_variable(variable_2)
        child2.add_variable(variable_1)

        return child1, child2
