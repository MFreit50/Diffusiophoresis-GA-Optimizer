from abc import ABC, abstractmethod
import numpy as np
import random # TODO Remove this import and use numpy instead
from diffusiophoresis.equation import Equation

class CrossoverStrategy(ABC):
    @abstractmethod
    def crossover(self, parent1: Equation, parent2: Equation) -> tuple[Equation, Equation]:
        pass

class UniformCrossover(CrossoverStrategy):
    def crossover(self, parent1: Equation, parent2: Equation) -> tuple[Equation, Equation]:

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
    def crossover(self, parent1 : Equation, parent2 : Equation) -> tuple[Equation, Equation]:

        # Get the genes of the parents
        parent1_genes = parent1.get_variable_list()
        parent2_genes = parent2.get_variable_list()
        
        child1 = Equation()
        child2 = Equation()
        
        # Randomly select a crossover point
        random_crossover_point = random.randint(1, len(parent1_genes)-1)
        child1_genes = parent1_genes[:random_crossover_point] + parent2_genes[random_crossover_point:]
        child2_genes = parent2_genes[:random_crossover_point] + parent1_genes[random_crossover_point:]
        
        child1.set_variable_list(child1_genes)
        child2.set_variable_list(child2_genes)

        return child1, child2
