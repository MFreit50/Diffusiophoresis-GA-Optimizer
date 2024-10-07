import numpy as np
import concurrent.futures
import random
from diffusiophoresis.equation import Equation
from diffusiophoresis.variable import Variable

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
        self.fitness_scores: list = []
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
        self.fitness_scores = self.evaluate_population_fitness(self.population)
    
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
            
            #print("population size: ", len(self.population))

            self.population = new_population

            # Evaluate the fitness of the new population
            fitness_results = self.evaluate_population_fitness(new_population)
            self.fitness_scores = fitness_results

            sorted_population = self.sort_population_by_fitness(new_population, fitness_results)
            self.best_equation = sorted_population[0]

            # Adjust mutation rate based on population diversity
            unique_fitness_results = len(set(fitness_results))
            if unique_fitness_results < self.population_size * 0.10:  # Low diversity
                #self.mutation_rate = min(self.mutation_rate * 1.1, 0.5)
                pass
            else:
                #self.mutation_rate = max(self.mutation_rate * 0.9, 0.01)
                pass
            
            self.broadcast_data(generation, fitness_results)

        print(self.best_equation)

    def select_parents(self) -> tuple:
        """
        Select two parent equations from the population based on fitness.

        Considerations:
            - Selection strategy: Tournament selection, roulette wheel selection, or rank-based selection.
            - Parents should have a higher probability of being selected if they have higher fitness.
        
        Returns:
            tuple: Two equations selected for crossover.
        """
        method_list: list = ["tournament", "roulette"]
        method = random.choice(method_list)
        #print("method: ", method)
        parent1 = None
        parent2 = None
        if(method == "tournament"):
            parent1, parent2 = self.tournament_selection(tournament_size=6)
        elif(method == "roulette"):
            parent1, parent2 = self.roulette_selection()
        else:
            raise NotImplementedError("This selection method is either invalid or not implemented yet!")

        return parent1, parent2

    def roulette_selection(self):
        #Step 1: calculate total fitness
        total_fitness: float = sum(fitness for fitness in self.fitness_scores)

        #Step 2: calculate cummulative probabilities
        cummulative_probabilities: list = []
        cummulative_sum: float = 0
        for fitness in self.fitness_scores:
            normalized_probability: float = fitness / total_fitness
            cummulative_sum += normalized_probability
            cummulative_probabilities.append(cummulative_sum)

        #Step 3: select individual randomly
        def roulette_select_parent():
            random_value = random.random()
            for i, cummulative_probability in enumerate(cummulative_probabilities):
                if random_value <= cummulative_probability:
                    return self.population[i]
        
        parent1 = roulette_select_parent()
        parent2 = roulette_select_parent()

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

    def crossover(self, parent1: Equation, parent2: Equation) -> tuple:
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
        variable_list = child.get_variable_list()
        filtered_variables = [var for var in variable_list if not var.is_constant()]
        
        #choose a variable randomly
        chosen_variable: Variable = random.choice(filtered_variables)
        
        #add a small positive or negative step to the value
        current_value = chosen_variable.get_value()
        step_size = random.uniform(-0.001, 0.001)
        
        #ensure the new value stays within the bounds of max/min range
        new_value = np.clip(current_value + step_size, chosen_variable.get_min_range(), chosen_variable.get_max_range())
        chosen_variable.set_value(new_value)

        child.add_variable(chosen_variable)
        return child

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
    
    def sort_population_by_fitness(self, population, fitness_scores):
        """
        Returns a new population sorted by their fitness scores in descending order.
        """
        paired_population = list(zip(fitness_scores, population))
        sorted_population = sorted(paired_population, key=lambda x: x[0], reverse=True)
        return [individual for _, individual in sorted_population]
        
    def broadcast_data(self, generation : int, fitness_results : list) -> None:
        data = {
                "generation": generation + 1,
                "best_fitness": self.evaluate_fitness(self.best_equation),
                "mutation_rate": self.mutation_rate,
                "unique_fitness_scores": len(set(fitness_results))
            }
            
        #Broadcast the data to listeners
        self.broadcaster.broadcast(data)