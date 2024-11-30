import random
import numpy as np
from diffusiophoresis.equation import Equation
from diffusiophoresis.variable import Variable
from abc import ABC, abstractmethod

class MutationStrategy(ABC):
    @abstractmethod
    def mutate(self, individual: list, bounds: list[tuple]) -> Equation:
        pass

class RandomizeMutation(MutationStrategy):
    def mutate(self, individual: list, bounds: list[tuple]) -> Equation:
        # For each variable, generate a random value within the given bounds
        individual = [random.uniform(min, max) for min, max in bounds]
        return individual
    
class StepMutation(MutationStrategy):
    def mutate(self, individual: list, bounds: list[tuple]) -> list:
        # Choose an index randomly
        i = random.randint(0, len(individual) - 1)
        
        # Get the max and min range of the chosen variable
        chosen_variable_max: float = bounds[i][1]
        chosen_variable_min: float = bounds[i][0]
        
        # Calculate the step size and value for the mutation
        step_factor: float = 0.1
        step_size: float = step_factor * (chosen_variable_max - chosen_variable_min)
        step_value: float = random.uniform(-step_size, step_size)
        
        # Ensure the new value stays within the bounds of max/min range
        new_value: float = np.clip(individual[i] + step_value, 
                                   chosen_variable_min, 
                                   chosen_variable_max)
        
        individual[i] = new_value
        
        return individual
    
