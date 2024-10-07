import numpy as np
import concurrent.futures
import random
from diffusiophoresis.equation import Equation

class GeneticAlgorithm:
    def __init__(self, generations: int, population_size: int, crossover_rate: float, mutation_rate: float, broadcaster):
        """
        Initialize the Genetic Algorithm.

        Args:
            generations (int): The number of generations to evolve the population.
            population_size (int): The number of individuals (equations) in the population.
            crossover_rate (float): The probability (0.0 to 1.0) that crossover will occur between two individuals during reproduction.
            mutation_rate (float): The probability (0.0 to 1.0) that a mutation will occur in an individual's variables after crossover.

        Attributes:
            generations (int): The number of generations to evolve the population.
            population_size (int): The number of individuals in the population.
            crossover_rate (float): The likelihood that crossover will occur when generating offspring.
            mutation_rate (float): The likelihood that mutation will occur in an offspring's variables.
            population (list): The current population of equations (individuals) being evolved.
            best_equation (Equation): The best solution (Equation) found during evolution based on fitness.
            cached_fitness (dict): A cache that stores pre-calculated fitness scores of individuals for performance optimization.
        """
        self.generations: int = generations
        self.population_size: int = population_size
        self.crossover_rate: float = crossover_rate
        self.mutation_rate: float = mutation_rate
        self.population: list = []
        self.best_equation: Equation = None

        self.cached_fitness: dict = {}

        self.broadcaster = broadcaster
    
    def run(self) -> Equation:
        """
        Run the genetic algorithm to evolve the population and find the best solution.

        This method initializes the population, evolves it over multiple generations, and 
        returns the best equation found.
        
        Returns:
            best_equation: The equation with the highest fitness after all generations.
        """
        self.initialize_population()
        self.evolve()
        return self.best_equation

    def initialize_population(self):
        """
        Initialize the population by filling it with equations that contain randomized variables.

        This method fills the population with random equations created by the
        create_random_equation method.
        """
        self.population = [Equation().randomize_equation() for _ in range(self.population_size)]
    
    def evolve(self):
        """
        Evolve the population over several generations to optimize the solution.

        The method evolves the population using selection, crossover, and mutation.
        It also adjusts the mutation rate dynamically based on the diversity of the population.
        At each generation, the population is sorted by fitness, and the best individual is stored.

        Considerations:
            - Ensure a balance between exploration (mutation) and exploitation (selection).
            - Mutation rate adjustment helps to avoid local optima.
            - Crossover and mutation methods need to be clearly defined to ensure meaningful offspring.
        """
        for generation in range(self.generations):
            new_population: list = []

            # Create a new population via selection, crossover, and mutation
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents() 
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1) 
                child2 = self.mutate(child2)
                new_population.extend([child1, child2])

            # Evaluate the fitness of the new population
            fitness_results = self.evaluate_population_fitness(new_population)

            # Sort population based on fitness and keep the best individuals
            new_population = [equation for equation in sorted(zip(fitness_results, new_population), key=lambda x: x[0], reverse=True)]
            _, self.best_equation = new_population[0]

            # Adjust mutation rate based on population diversity
            unique_fitness_results = len(set(fitness_results))
            if unique_fitness_results < self.population_size * 0.10:  # Low diversity
                self.mutation_rate = min(self.mutation_rate * 1.1, 0.5)
            else:
                self.mutation_rate = max(self.mutation_rate * 0.9, 0.01)
            
            self.broadcast_data(generation, fitness_results)

        print(self.best_equation)

    def select_parents(self, method:str="tournament") -> tuple:
        """
        Select two parent equations from the population based on fitness.

        Considerations:
            - Selection strategy: Tournament selection, roulette wheel selection, or rank-based selection.
            - Parents should have a higher probability of being selected if they have higher fitness.
        
        Returns:
            tuple: Two equations selected for crossover.
        """

        parent1 = None
        parent2 = None
        if(method == "tournament"):
            parent1, parent2 = self.tournament_selection(tournament_size=6)
        else:
            raise NotImplementedError("This selection method is either invalid or not implemented yet!")

        return parent1, parent2

    def tournament_selection(self, tournament_size: int) -> tuple:
        """
        Perform tournament selection to choose top individuals from a population

        Args:
            tournament_size: The number of individuals participating in the tournament

        Returns: tuple: A tuple containing the selected individuals
        """
        
        # First tournament
        tournament_contestants1 = random.sample(self.population, tournament_size)
        parent1 = max(tournament_contestants1, key=lambda individual: self.evaluate_fitness(individual))

        #Remove the first parent from the population
        population_without_parent1 = [individual for individual in self.population if individual != parent1]

        #Second tournament
        tournament_contestants2 = random.sample(population_without_parent1, tournament_size)
        parent2 = max(tournament_contestants2, key=lambda individual: self.evaluate_fitness(individual))

        return parent1, parent2     

    def crossover(self, parent1: Equation, parent2: Equation, method:str="uniform") -> tuple:
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

        if np.random.rand() > self.crossover_rate:
            return parent1, parent2
            
        if(method == "uniform"): 
            child1, child2 = self.uniform_crossover(parent1, parent2)
            return child1, child2
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

    def mutate(self, child: Equation, method:str="swap") -> Equation:
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
        
        return child.randomize_equation()
        ##code below does not function as intended
        if(method == "swap"):
            child = self.swap_mutation(child)
            return child
        else:
            raise NotImplementedError("This mutation method is either invalid or not implemented yet!")

    def swap_mutation(self, child: Equation) -> Equation:
        """
        Perform swap mutation on the given equation and return a new mutated equation.

        Args:
            child (Equation): The equation object to mutate.

        Returns:
            Equation: A new equation object with swapped variable values.
        """
        mutated_child = child
        variable_list = child.get_variable_list()
        variable_list = [variable for variable in variable_list if not variable.is_constant()]#Filter out constant variables
        
        index1, index2 = random.sample(range(len(variable_list)), 2)

        variable1 = variable_list[index1]
        variable2 = variable_list[index2]

        variable1_name = variable1.get_name()
        variable2_name = variable2.get_name()

        mutated_child.set_value(variable2_name, variable1.get_value())
        mutated_child.set_value(variable1_name, variable2.get_value())
        
        return mutated_child


    def evaluate_population_fitness(self, population: list) -> list:
        """
        Evaluate the fitness of the entire population in parallel using multithreading.

        This method uses a thread pool to concurrently evaluate the fitness of each individual 
        in the population, improving performance for large populations.
        
        Args:
            population (list): A list of equations representing the population.
        
        Returns:
            fitness_results (list): A list of fitness scores for the population.
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            fitness_results = list(executor.map(self.evaluate_fitness, population))
        return fitness_results

    def evaluate_fitness(self, equation: Equation) -> float:
        """
        Evaluate the fitness of a single equation.

        This method should compute a fitness score for the equation based on how well 
        it solves the target problem.
        
        Considerations:
            - Define the fitness function: How do you measure how "good" an equation is?
            - The fitness function should guide the evolution toward the optimal solution.
        
        Args:
            equation: The equation to evaluate.
        
        Returns:
            fitness_score: A numeric score representing the fitness of the equation.
        """
        if equation in self.cached_fitness:
            return self.cached_fitness[equation]
        
        #fitness: float = equation.optimize()
        
        fitness : float = equation.get_diffusiophoretic_velocity()
        self.cached_fitness[equation] = fitness
        
        return fitness
        
    def broadcast_data(self, generation : int, fitness_results : list) -> None:
        data = {
                "generation": generation + 1,
                "best_fitness": self.evaluate_fitness(self.best_equation),
                "mutation_rate": self.mutation_rate,
                "unique_fitness_scores": len(set(fitness_results))
            }
            
        #Broadcast the data to listeners
        self.broadcaster.broadcast(data)