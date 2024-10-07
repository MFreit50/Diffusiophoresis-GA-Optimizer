import random
import numpy as np
from equation import Equation
from variable import Variable


class Mutation:
    def mutate(self, child: Equation) -> Equation:
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

        if np.random.rand() > self.mutation_rate:
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
        #get non constant variables from equation
        variable_list = child.get_variable_list(filter_constants=True)
        
        #choose a variable randomly
        chosen_variable: Variable = random.choice(variable_list)
        
        #add a small positive or negative step to the value
        current_value = chosen_variable.get_value()
        step_size = random.uniform(-0.001, 0.001)
        
        #ensure the new value stays within the bounds of max/min range
        new_value = np.clip(current_value + step_size, chosen_variable.get_min_range(), chosen_variable.get_max_range())
        chosen_variable.set_value(new_value)

        child.add_variable(chosen_variable)
        return child