import copy
import numpy as np
import concurrent.futures
import random
from diffusiophoresis.equation import Equation
from diffusiophoresis.variable import Variable
from ga.strategy_manager import StrategyManager
from ga.data_aggregator import DataAggregator

class GeneticAlgorithm:
    def __init__(self, generations: int, population_size: int, strategy_manager : StrategyManager, data_aggregator : DataAggregator = None):
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
        self.strategy_manager = strategy_manager
        self.data_aggregator = data_aggregator

        self.generations: int = generations
        self.population_size: int = population_size
        self.population: list = []
        self.fitness_scores: list = []
        self.best_equation: Equation = None
        self.cached_fitness: dict = {}

        self.no_improvement_counter : int = None
        self.best_equation : Equation = None
        self.previous_best_equation : Equation = None
    
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
            if generation%100 == 0:
                self.cached_fitness.clear()

            # Evolve Population
            selected_parents = self.strategy_manager.select_parents(self.population, self.fitness_scores)
            offspsring = self.strategy_manager.crossover(selected_parents)
            mutated_population = self.strategy_manager.mutate(offspsring)
            self.population = mutated_population
            
            # Evaluate Population Fitness
            self.fitness_scores = self.evaluate_population_fitness(self.population)
            if self.all_unique_memory_addresses(self.population) == False:
                raise KeyError("all should be unique")

            # Update Best Equation
            self.update_best_equation()

            # Update Data Aggregator and Strategy Manager
            unique_individuals_count = len(set(self.population))
            self.strategy_manager.update_strategies(unique_individuals_count, self.fitness_scores, self.population_size)

            if self.data_aggregator is not None:
                self.collect_data(generation, unique_individuals_count)
                self.data_aggregator.broadcast_data()
                print(self.data_aggregator)

            # Check Termination Function
            if self.evaluate_termination() == True:
                break

        print(self.best_equation)

    def update_best_equation(self):
        sorted_population = self.sort_population_by_fitness(self.population, self.fitness_scores)
        self.previous_best_equation = copy.deepcopy(self.best_equation)
        self.best_equation = sorted_population[0]

        if self.previous_best_equation == self.best_equation:
            self.no_improvement_counter += 1
        else:
            self.no_improvement_counter = 0

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
        
        fitness : float = equation.optimize()

        self.cached_fitness[equation] = fitness
        
        return fitness
    
    def collect_data(self, generation, unique_individuals_count):
        self.data_aggregator.log("generation", generation)
        self.data_aggregator.log("best_fitness", self.evaluate_fitness(self.best_equation))
        self.data_aggregator.log("mutation_rate", self.strategy_manager.get_mutation_rate())
        self.data_aggregator.log("crossover_rate", self.strategy_manager.get_crossover_rate())
        self.data_aggregator.log("unique_individuals_count", unique_individuals_count)
        self.data_aggregator.analyze_genetic_algorithm(self.population, self.fitness_scores)

    def evaluate_termination(self):
        max_no_improvement: int = 100
        no_improvement_counter: int = self.data_aggregator.get("no_improvement_counter")

        if no_improvement_counter > max_no_improvement:
            print(f"Stopping due to no improvement for {no_improvement_counter} generations.")
            return True

    def sort_population_by_fitness(self, population, fitness_scores):
            """
            Returns a new population sorted by their fitness scores in descending order.
            """
            paired_population = list(zip(fitness_scores, population))
            sorted_population = sorted(paired_population, key=lambda x: x[0], reverse=True)

            sorted_individuals = [individual for _, individual in sorted_population]

            return sorted_individuals
    
    def subscribe(self, subscriber):
        if self.data_aggregator == None:
            raise ValueError("Missing Data Aggregator, cannot subscribe component")
        
        self.data_aggregator.subscribe(subscriber)
    
    def all_unique_memory_addresses(self, objects): #debugging purposes
        return len(objects) == len(set(id(obj) for obj in objects))