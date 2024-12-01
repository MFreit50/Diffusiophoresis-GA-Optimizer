import copy
import numpy as np
import concurrent.futures
from typing import List, Optional, Union
from diffusiophoresis.equation import Equation
from diffusiophoresis.variable import Variable
from ga.strategy_manager import StrategyManager
from ga.data_aggregator import DataAggregator

class GeneticAlgorithm:
    def __init__(self, generations: int, population_size: int, strategy_manager: StrategyManager, data_aggregator: Optional[DataAggregator] = None):
        """
        Initialize the Genetic Algorithm.

        Args:
            generations (int): The number of generations to evolve the population.
            population_size (int): The number of individuals (equations) in the population.
            strategy_manager (StrategyManager): Manages selection, crossover, and mutation strategies.
            data_aggregator (DataAggregator, optional): Collects and logs data during the algorithm's run.
        
        Attributes:
            generations (int): The number of generations to evolve the population.
            population_size (int): The number of individuals in the population.
            population (list): The current population of equations (individuals) being evolved.
            fitness_scores (list): List of fitness scores for the population.
            best_equation (Equation): The best solution (Equation) found during evolution based on fitness.
            cached_fitness (dict): A cache that stores pre-calculated fitness scores of individuals for performance optimization.
        """
        self.strategy_manager = strategy_manager
        self.data_aggregator = data_aggregator

        self.generations: int = generations
        self.population_size: int = population_size
        self.population: List[Equation] = []
        self.fitness_scores: List[float] = []
        self.best_equation: Equation = Equation()
        self.cached_fitness: dict = {}

        self.no_improvement_counter: int = 0
        self.last_best_equations: List[Equation] = []
    
    def run(self) -> Equation:
        """
        Run the genetic algorithm to evolve the population and find the best solution.

        Returns:
            Equation: The equation with the highest fitness after all generations.
        """
        self.initialize_population()
        self.evolve()
        return self.best_equation

    def initialize_population(self) -> None:
        """
        Initialize the population by filling it with equations that contain randomized variables.
        """
        self.population = [Equation().randomize_equation() for _ in range(self.population_size)]
        self.fitness_scores = self.evaluate_population_fitness(self.population)

    def evolve(self) -> None:
        """
        Evolve the population over several generations to optimize the solution.
        """
        for generation in range(self.generations):
            if generation % 100 == 0:
                self.cached_fitness.clear()

            selected_parents = self.strategy_manager.select_parents(self.population, self.fitness_scores)
            offspring = self.strategy_manager.crossover(selected_parents)
            mutated_population = self.strategy_manager.mutate(offspring)
            self.population = mutated_population
            
            self.fitness_scores = self.evaluate_population_fitness(self.population)
            if not self.all_unique_memory_addresses(self.population):
                raise KeyError("All individuals should be unique.")

            self.update_best_equation()

            unique_individuals_count = len(set(self.population))
            self.strategy_manager.update_strategies(unique_individuals_count, self.fitness_scores, self.population_size)

            if self.data_aggregator is not None:
                self.collect_data(generation, unique_individuals_count)
                self.data_aggregator.broadcast_data()
                print(self.data_aggregator)

            if self.evaluate_termination():
                break
        
        print("before binary search")
        print(self.best_equation, self.best_equation.optimize())
        
        print("after binary search")
        binary_search_equation = self.binary_search(self.best_equation)
        print(binary_search_equation, binary_search_equation.optimize())
        
        print("after hill climb")
        hill_climbed_equation = self.hill_climb(self.best_equation)
        print(hill_climbed_equation, hill_climbed_equation.optimize())
        
    def update_best_equation(self) -> None:
        """
        Update the best equation based on the current population.
        """
        sorted_population = self.sort_population_by_fitness(self.population, self.fitness_scores)
        self.last_best_equations.append(copy.deepcopy(self.best_equation))
        
        self.best_equation = sorted_population[0]
        
        if self.last_best_equations[-1] == self.best_equation:
            self.no_improvement_counter += 1
        else:
            self.no_improvement_counter = 0
            
        if len(self.last_best_equations) > 30:
            self.last_best_equations.pop(0)    

    def evaluate_population_fitness(self, population: List[Equation]) -> List[float]:
        """
        Evaluate the fitness of the entire population in parallel using multithreading.

        Args:
            population (List[Equation]): A list of equations representing the population.
        
        Returns:
            List[float]: A list of fitness scores for the population.
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            fitness_results = list(executor.map(self.evaluate_fitness, population))
        return fitness_results

    def evaluate_fitness(self, equation: Equation) -> float:
        """
        Evaluate the fitness of a single equation.

        Args:
            equation (Equation): The equation to evaluate.
        
        Returns:
            float: A numeric score representing the fitness of the equation.
        """
        if equation in self.cached_fitness:
            return self.cached_fitness[equation]
        
        fitness: float = equation.optimize()
        self.cached_fitness[equation] = fitness
        
        return fitness
    
    def collect_data(self, generation: int, unique_individuals_count: int) -> None:
        """
        Collect and log data for each generation.

        Args:
            generation (int): The current generation number.
            unique_individuals_count (int): The number of unique individuals in the population.
        """
        self.data_aggregator.log("generation", generation)
        self.data_aggregator.log("best_fitness", self.evaluate_fitness(self.best_equation))
        self.data_aggregator.log("mutation_rate", self.strategy_manager.get_mutation_rate())
        self.data_aggregator.log("crossover_rate", self.strategy_manager.get_crossover_rate())
        self.data_aggregator.log("unique_individuals_count", unique_individuals_count)
        self.data_aggregator.analyze_genetic_algorithm(self.population, self.fitness_scores)

    def evaluate_termination(self) -> bool:
        """
        Evaluate whether to terminate the evolution process based on improvement metrics.

        Returns:
            bool: True if the termination condition is met, otherwise False.
        """
        max_no_improvement: int = 100

        if self.no_improvement_counter >= max_no_improvement:
            print(f"Stopping due to no improvement for {self.no_improvement_counter} generations.")
            return True
        return False

    def sort_population_by_fitness(self, population: List[Equation], fitness_scores: List[float]) -> List[Equation]:
        """
        Sort the population by fitness scores in descending order.

        Args:
            population (List[Equation]): The population of equations.
            fitness_scores (List[float]): The fitness scores corresponding to the population.
        
        Returns:
            List[Equation]: The population sorted by fitness.
        """
        paired_population = list(zip(fitness_scores, population))
        sorted_population = sorted(paired_population, key=lambda x: x[0], reverse=True)
        return [individual for _, individual in sorted_population]
    
    def subscribe(self, subscriber: object) -> None:
        """
        Subscribe a component to the data aggregator.

        Args:
            subscriber (object): The component to subscribe.
        
        Raises:
            ValueError: If data_aggregator is missing.
        """
        if self.data_aggregator is None:
            raise ValueError("Missing Data Aggregator, cannot subscribe component.")
        
        self.data_aggregator.subscribe(subscriber)
    
    def all_unique_memory_addresses(self, objects: List[object]) -> bool:
        """
        Check if all objects have unique memory addresses.

        Args:
            objects (List[object]): The list of objects to check.
        
        Returns:
            bool: True if all objects have unique memory addresses, otherwise False.
        """
        return len(objects) == len(set(id(obj) for obj in objects))
    

    def hill_climb(self, equation: Equation, max_iterations: int = 100) -> Equation:
        """
        Perform hill climbing to optimize the given equation.

        Args:
            max_iterations (int): Maximum number of iterations for hill climbing.
            step_size (float): The step size to explore neighboring solutions.

        Returns:
            Equation: The optimized equation after hill climbing.
        """
        current_equation = copy.deepcopy(equation)
        current_fitness = current_equation.optimize()
        current_equation_list = current_equation.get_variable_list(filter_constants=True)
        
        for iteration in range(max_iterations):
            print(f"Iteration: {iteration}")
            improved = False
            
            # Loop through each variable to optimize it
            for var in current_equation_list:
                print(f"Optimizing variable: {var.get_name()}")
                original_value = var.get_value()
                best_value = original_value  # Track the best value for this variable
                
                step_size = GeneticAlgorithm.get_msd_step_size(original_value)  # Get the most significant digit after the decimal point
                
                # Try moving the variable up and down by step_size
                for delta in [-step_size, step_size]:
                    print(f"Trying delta: {delta}")
                    print(f"Original Value: {var.get_value()}")
                    var.set_value(original_value + delta)
                    print(f"New Value: {var.get_value()}")
                    current_equation.set_variable(var)
                    new_fitness = current_equation.optimize()
                    
                    if new_fitness > current_fitness:
                        current_fitness = new_fitness
                        best_value = var.get_value()
                        improved = True
                        print(f"Fitness Improved: {current_fitness}")
                    
                # Restore the best found value for this variable in this iteration
                print("Best Value At the End of Testing Steps in Both Directions: ", best_value)
                var.set_value(best_value)
            
            # If no improvement was found across all variables, stop early
            if not improved:
                print("No improvement found, stopping hill climbing.")
                break
            
        current_equation.set_variable_list(current_equation_list)
        return current_equation
    
    def binary_search(self, individual : Equation):

        def bs(low, middle, high, individual : Equation, var : Variable) -> Equation:
            def optimize(individual : Equation, var : Variable, value : float) -> float:
                var.set_value(value)
                individual.set_variable(var)
                return individual.optimize()
            
            if low == middle or high == middle:
                var.set_value(middle)
                individual.set_variable(var)
                return individual
            
            new_low = (middle+low)/2
            new_high = (middle+high)/2
            
            new_low_score = optimize(individual, var, new_low)
            new_high_score = optimize(individual, var, new_high)

            if new_low_score > new_high_score:
                return bs(low, new_low, middle, individual, var)
            else:
                return bs(middle, new_high, high, individual, var)
        
        individual = copy.deepcopy(individual)
        variable_list = individual.get_variable_list(filter_constants=True)

        for var in variable_list:

            middle = var.get_value()
            low = middle - 0.1 if var.is_within_range(middle - 0.1) else middle
            high= middle + 0.1 if var.is_within_range(middle + 0.1) else middle

            individual = bs(low, middle, high, individual, var)

        return individual
    
    @staticmethod
    def get_msd_step_size(num):
        if num == 0:
            return 0  # Handle zero explicitly
        abs_num = abs(num)  # Work with positive values
        decimal_part = abs_num - int(abs_num)  # Get the fractional part only
        away_from_decimal = 0

        while decimal_part < 1 and decimal_part != 0:
            decimal_part *= 10
            away_from_decimal += 1

        step_size = 10 ** -away_from_decimal
        print(f"Step Size: {step_size}")
        return step_size
