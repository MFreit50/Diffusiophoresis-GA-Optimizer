import random
import numpy as np
from diffusiophoresis.equation import Equation
from diffusiophoresis.variable import Variable


class Mutation:
    def mutate(self, mutation_rate: float, child: Equation) -> Equation:
        """
        Mutate a child equation to introduce variation.

        Considerations:
            - Mutation rate: How frequently mutations should happen.
            - Mutation strategy: Randomly alter coefficients, add/remove terms, or other changes.
            - Ensure the mutation does not produce an invalid equation.
        
        Args:
            child: The equation to be mutated.
        
        Returns:
            mutated_child: The mutated equation.
        """

        #TODO Have mutate() handle an input of an array of Equations

        if np.random.rand() > mutation_rate:
            return child
        
        methods = ["randomize", "step", "step", "step"]
        method = random.choice(methods)
        #print("method: ", method)

        ##code below does not function as intended
        if(method == "randomize"):
            return self.randomize_mutation(child)
        elif(method == "step"):
            return self.step_mutation(child)
        else:
            raise NotImplementedError("This mutation method is either invalid or not implemented yet!")

    def randomize_mutation(self, child: Equation) -> Equation:
        return child.randomize_equation()

    def step_mutation(self, child: Equation) -> Equation:
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