import random
import numpy as np

from diffusiophoresis.equation import Equation


class Crossover:
    def crossover(self, crossover_rate : float, parent1: Equation, parent2: Equation) -> tuple:
        """
        Perform crossover (recombination) between two parent equations to produce a child.

        Considerations:
            - How to combine the genetic material (equation components) from both parents.
            - Single-point, two-point, or uniform crossover strategies.
            - Ensure that the crossover results in a valid equation.
        
        Args:
            parent1: The first parent equation.
            parent2: The second parent equation.
        
        Returns:
            child: The newly generated equation after crossover.
        """
        if np.random.rand() > crossover_rate:
            return parent1, parent2
        
        methods = ["uniform", "single_point"]
        method = random.choice(methods)
        #print("method: ", method)
        if(method == "uniform"): 
            child1, child2 = self.uniform_crossover(parent1, parent2)
            return child1, child2
        elif(method == "single_point"):
            return self.single_point_crossover(parent1, parent2)
        else:
            raise NotImplementedError("This crossover method is either invalid or not implemented yet!")

    def uniform_crossover(self, parent1: Equation, parent2: Equation) -> tuple:
        """
        Perform uniform crossover between two parent Equation objects.

        Args:
            parent1 (Equation): The first parent individual.
            parent2 (Equation): The second parent individual.

        Returns:
            child1, child2 (Equation, Equation): The two offspring created from the uniform crossover of the two parents.
        """

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

    def single_point_crossover(self, parent1 : Equation, parent2 : Equation) -> Equation:
        #aquire 1 variable from each parent
        variable_1 = random.choice(parent1.get_variable_list(filter_constants=True))
        variable_2 = random.choice(parent2.get_variable_list(filter_constants=True))

        #switch the variable between parents to create child
        child1 = parent1
        child2 = parent2

        child1.add_variable(variable_2)
        child2.add_variable(variable_1)

        return child1, child2