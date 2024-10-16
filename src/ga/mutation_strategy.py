import random
import numpy as np
from diffusiophoresis.equation import Equation
from diffusiophoresis.variable import Variable
from abc import ABC, abstractmethod

class MutationStrategy(ABC):
    @abstractmethod
    def mutate(self, mutation_rate: float, child: Equation) -> Equation:
        pass

class RandomizeMutation(MutationStrategy):
    def mutate(self, mutation_rate: float, child: Equation) -> Equation:
        if np.random.rand() > mutation_rate:
            return child
        return child.randomize_equation()
    
class StepMutation(MutationStrategy):
    def mutate(self, child: Equation) -> Equation:
        #get non constant variables from equation
        variable_list = child.get_variable_list(filter_constants=True)
        
        #choose a variable randomly
        chosen_variable: Variable = random.choice(variable_list)
        
        #add a small positive or negative step to the value
        current_value = chosen_variable.get_value()
        #TODO: A step of +-0.001 is too small for variables with larger range

        step_size = random.uniform(-0.001, 0.001)
        
        #ensure the new value stays within the bounds of max/min range
        new_value = np.clip(current_value + step_size, chosen_variable.get_min_range(), chosen_variable.get_max_range())
        chosen_variable.set_value(new_value)

        child.add_variable(chosen_variable)
        return child