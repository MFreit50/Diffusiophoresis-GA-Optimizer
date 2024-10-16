import copy
import numpy as np
import concurrent.futures
import random
from diffusiophoresis.equation import Equation
from diffusiophoresis.variable import Variable
from ga.crossover import Crossover
from ga.mutation import Mutation
from ga.selection import Selection

class GeneticAlgorithm:
    def __init__(self, generations: int, population_size: int, crossover_rate: float, mutation_rate: float, broadcaster=None):
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
        #Components
        self.mutation_strategy = Mutation()
        self.crossover_strategy = Crossover()
        self.selection_strategy = Selection()

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
        
        previous_best_fitness: float = 0
        no_improvement_counter: int = 0

        for generation in range(self.generations):
            new_population: list = []

            # Create a new population via selection, crossover, and mutation
            while len(new_population) < self.population_size:
                parent1, parent2 = self.selection.select_parents(self.population, self.fitness_scores)
                child1, child2 = self.crossover.crossover(self.crossover_rate, parent1, parent2)
                child1 = self.mutation.mutate(self.mutation_rate, child1)
                child2 = self.mutation.mutate(self.mutation_rate, child2)
                new_population.extend([child1, child2])

            #print("population size: ", len(self.population))

            self.population = new_population

            # Evaluate the fitness of the new population
            fitness_results = self.evaluate_population_fitness(new_population)
            self.fitness_scores = fitness_results
            
            # Sort the population by fitness and update the best equation
            sorted_population = self.sort_population_by_fitness(new_population, fitness_results)
            self.best_equation = sorted_population[0]

            # Check for improvement 
            should_stop: bool = False
            should_stop, no_improvement_counter = self.check_for_improvement(previous_best_fitness, no_improvement_counter)
            if should_stop:
                print(f"Stopping due to no improvement for {no_improvement_counter} generations.")
                break
            previous_best_fitness = self.evaluate_fitness(self.best_equation)

            # Adjust mutation rate based on population diversity
            unique_fitness_results = len(set(fitness_results))
            if unique_fitness_results < self.population_size * 0.15:  # Low diversity
                self.mutation_rate = min(self.mutation_rate * 1.1, 0.5)
                pass
            else:
                self.mutation_rate = max(self.mutation_rate * 0.9, 0.01)
                pass
            
            if not self.broadcaster:
                return
            
            self.broadcast_data(generation, fitness_results)

        print(self.best_equation)

    def check_for_improvement(self, previous_best_fitness, no_improvement_counter):
        max_no_improvement: int = 100
        if self.evaluate_fitness(self.best_equation) > previous_best_fitness:
            no_improvement_counter = 0
            return False, no_improvement_counter
        else:
            no_improvement_counter += 1
            return no_improvement_counter > max_no_improvement, no_improvement_counter

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