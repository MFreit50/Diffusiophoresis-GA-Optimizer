import random
import numpy as np
from diffusiophoresis.equation import Equation
from diffusiophoresis.variable import Variable
from abc import ABC, abstractmethod

class MutationStrategy(ABC):
    @abstractmethod
    def mutate(self, child: Equation) -> Equation:
        pass

class RandomizeMutation(MutationStrategy):
    def mutate(self, child: Equation) -> Equation:
        return child.randomize_equation()
    
class StepMutation(MutationStrategy):
    def mutate(self, child: Equation) -> Equation:
        
        # Get non constant variables from equation
        variable_list: list[Variable] = child.get_variable_list(filter_constants=True)
        
        # Choose a variable randomly
        chosen_variable: Variable = random.choice(variable_list)
        
        # Get the max and min range of the chosen variable
        chosen_variable_max: float = chosen_variable.get_max_range()
        chosen_variable_min: float = chosen_variable.get_min_range()
        
        # Calculate the step size and value for the mutation
        step_factor: float = 0.1
        step_size: float = step_factor * (chosen_variable_max - chosen_variable_min)
        step_value: float = random.uniform(-step_size, step_size)
        
        # Ensure the new value stays within the bounds of max/min range
        new_value: float = np.clip(chosen_variable.get_value() + step_value, 
                                   chosen_variable_min, 
                                   chosen_variable_max)
        
        chosen_variable.set_value(new_value)
        child.add_variable(chosen_variable)
        
        return child