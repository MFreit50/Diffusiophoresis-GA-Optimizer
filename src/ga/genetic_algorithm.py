import copy
import random
import concurrent.futures
from typing import List, Optional, Union
from ga.strategy_manager import StrategyManager
from ga.data_aggregator import DataAggregator
from scipy._lib._util import _FunctionWrapper, MapWrapper

def genetic_algorithm(func: callable, bounds: list[tuple], args: tuple = (), generations: int = 1000, population_size: int = 15, data_aggregator: Optional[DataAggregator] = None):
    with GeneticAlgorithm(func,bounds,args,generations,population_size,data_aggregator) as genetic_algorithm:
        ret = genetic_algorithm.optimize()
    return ret

class GeneticAlgorithm:
    def __init__(self, func: callable, bounds: list[tuple], args: tuple = (), generations: int = 1000, population_size: int = 15, data_aggregator: Optional[DataAggregator] = None):
        self.func: _FunctionWrapper = _FunctionWrapper(func, args)
        self.bounds: list[tuple] = bounds
        self.num_variables: int = len(bounds)

        self.strategy_manager = StrategyManager()
        self.data_aggregator = data_aggregator

        self.generations: int = generations
        self.population_size: int = population_size
        self.population: list[float] = [[random.uniform(min, max) for min, max in self.bounds] for i in range(self.population_size)]

        self.cached_fitness: dict = {}
        self.fitness_scores: list[float] = self.evaluate_population_fitness(self.population)

        self.no_improvement_counter: int = 0

        self.best_individual = []
        self.previous_best_individuals = []

    def optimize(self) -> None:
        """
        Evolve the population over several generations to optimize the solution.
        """
        for generation in range(self.generations):

            if generation % 100 == 0:
                self.cached_fitness.clear()

            parents = self.strategy_manager.select_parents(self.population, self.fitness_scores)
            offspring = self.strategy_manager.crossover(parents)
            mutated_population = self.strategy_manager.mutate(offspring, self.bounds)
            self.population = mutated_population

            self.fitness_scores = self.evaluate_population_fitness(self.population)

            self.update_best_equation()
            
            unique_individuals_count = len(set(tuple(individual) for individual in self.population))
            self.strategy_manager.update_strategies(unique_individuals_count, self.fitness_scores, self.population_size)

            if self.data_aggregator is not None:
                self.collect_data(generation, unique_individuals_count)
                self.data_aggregator.broadcast_data()
                print(self.data_aggregator)

            if self.evaluate_termination():
                break
        
        print("before binary search")
        print(self.best_individual, self.func(self.best_individual))
        
        print("after binary search")
        binary_search_equation = self.binary_search(self.best_individual)
        print(binary_search_equation, self.func(binary_search_equation))
        
        print("after hill climb")
        hill_climbed_equation = self.hill_climb(self.best_individual)
        print(hill_climbed_equation, self.func(hill_climbed_equation))
        return self.best_individual

    def update_best_equation(self) -> None:
        """
        Update the best equation based on the current population.
        """
        sorted_population = self.sort_population_by_fitness(self.population, self.fitness_scores)
        self.previous_best_individuals.append(copy.deepcopy(self.best_individual))
        self.best_individual = sorted_population[0]

        if self.previous_best_individuals[-1] == self.best_individual:
            self.no_improvement_counter += 1
        else:
            self.no_improvement_counter = 0
            
        if len(self.previous_best_individuals) > 30:
            self.previous_best_individuals.pop(0)    

    def evaluate_population_fitness(self, population: list) -> List[float]:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            fitness_results = list(executor.map(self.evaluate_fitness, population))
        return fitness_results

    def evaluate_fitness(self, individual) -> float:
        individual_tuple = tuple(individual)
        if individual_tuple in self.cached_fitness:
            return self.cached_fitness[individual_tuple]
        
        fitness: float = self.func(individual)
        self.cached_fitness[individual_tuple] = fitness

        return fitness
    
    def collect_data(self, generation: int, unique_individuals_count: int) -> None:
        """
        Collect and log data for each generation.

        Args:
            generation (int): The current generation number.
            unique_individuals_count (int): The number of unique individuals in the population.
        """
        self.data_aggregator.log("generation", generation)
        self.data_aggregator.log("best_fitness", self.evaluate_fitness(self.best_individual))
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

    def sort_population_by_fitness(self, population: List[float], fitness_scores: List[float]) -> List[float]:
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
    
    def hill_climb(self, individual: list, max_iterations: int = 100) -> list:
        """
        Perform hill climbing to optimize the given equation.

        Args:
            max_iterations (int): Maximum number of iterations for hill climbing.
            step_size (float): The step size to explore neighboring solutions.

        Returns:
            Equation: The optimized equation after hill climbing.
        """
        current_individual = copy.deepcopy(individual)
        current_fitness = self.func(individual)
        
        for iteration in range(max_iterations):
            #print(f"Iteration: {iteration}")
            improved = False
            
            # Loop through each variable to optimize it
            for i in range(len(individual)):
                var = individual[i]
                best_value = var  # Track the best value for this variable
                
                step_size = GeneticAlgorithm.get_msd_step_size(var)  # Get the most significant digit after the decimal point
                
                # Try moving the variable up and down by step_size
                for delta in [-step_size, step_size]:
                    #print(f"Trying delta: {delta}")
                    #print(f"Original Value: {var}")
                    var += delta
                    #print(f"New Value: {var}")
                    individual[i] = var
                    new_fitness = self.func(individual)
                    
                    if new_fitness > current_fitness:
                        current_fitness = new_fitness
                        best_value = var
                        improved = True
                        #print(f"Fitness Improved: {current_fitness}")
                    
                # Restore the best found value for this variable in this iteration
                #print("Best Value At the End of Testing Steps in Both Directions: ", best_value)
                var = best_value
            
            # If no improvement was found across all variables, stop early
            if not improved:
                #print("No improvement found, stopping hill climbing.")
                break
            
        return current_individual

    def binary_search(self, individual : list) -> list:

        def bs(low, middle, high, individual: list, gene_index: int) -> list:
            def optimize(individual: list, gene_index: int, value : float) -> float:
                individual[gene_index] = value
                return self.func(individual)
            
            if low == middle or high == middle:
                individual[gene_index] = middle
                return individual
            
            new_low = (middle+low)/2
            new_high = (middle+high)/2
            
            new_low_score = optimize(individual, gene_index, new_low)
            new_high_score = optimize(individual, gene_index, new_high)

            if new_low_score > new_high_score:
                return bs(low, new_low, middle, individual, gene_index)
            else:
                return bs(middle, new_high, high, individual, gene_index)
        
        individual = copy.deepcopy(individual)

        for i in range(len(individual)):
            min, max = self.bounds[i]
            middle = individual[i]
            low = middle - 0.1 if min < middle - 0.1 < max else middle
            high= middle + 0.1 if min < middle + 0.1 < max else middle
            individual = bs(low, middle, high, individual, i)

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

    #Magic Methods
    def __enter__(self):
        print("Running Genetic Algorithm")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Genetic Algorithm Finished")
        if exc_type:
            print("Exception Type:\n", exc_type,"\n")
            print("Exception Value:\n", exc_val,"\n")
            print("Exception Traceback:\n", exc_tb,"\n")

        return False