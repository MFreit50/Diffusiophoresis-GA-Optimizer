from abc import ABC, abstractmethod
import numpy as np
import random # TODO Remove this import and use numpy instead

class CrossoverStrategy(ABC):
    @abstractmethod
    def crossover(self, parent1, parent2):
        pass

class UniformCrossover(CrossoverStrategy):
    def crossover(self, parent1, parent2):
        # TODO: Debug: Check if both parents have the same variables for crossover

        child1 = []
        child2 = []

        for i in range(len(parent1)):
            if np.random.rand() < 0.5:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])

        return child1, child2

class SinglePointCrossover(CrossoverStrategy):
    def crossover(self, parent1 : list, parent2 : list):
        if len(parent1) != len(parent2):
            print("len1: ", len(parent1), " len2: ", len(parent2))
            raise ValueError("Parents must have the same length")

        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]

        return child1, child2
