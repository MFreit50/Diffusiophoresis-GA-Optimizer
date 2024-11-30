import random
import numpy as np
from diffusiophoresis.equation import Equation
from diffusiophoresis.variable import Variable


class Mutation:
    def mutate(self, mutation_rate: float, individual: list) -> list:
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
            return individual
        
        methods = ["randomize", "step", "step", "step"]
        method = random.choice(methods)
        #print("method: ", method)

        ##code below does not function as intended
        if(method == "randomize"):
            return self.randomize_mutation(individual)
        elif(method == "step"):
            return self.step_mutation(individual)
        else:
            raise NotImplementedError("This mutation method is either invalid or not implemented yet!")

    def randomize_mutation(self, individual: list, bounds: list[tuple]) -> list:
        individual.clear()

        # For each variable, generate a random value within the given bounds
        for lower, upper in bounds:
            randomized_value = np.random.uniform(lower, upper)
            individual.append(randomized_value)
        
        return individual

    def step_mutation(self, individual: list, bounds: list[tuple]) -> list:
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