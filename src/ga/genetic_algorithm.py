import copy
import random
import concurrent.futures
from typing import List, Optional, Union
from ga.strategy_manager import StrategyManager
from scipy._lib._util import _FunctionWrapper, MapWrapper
from scipy.optimize import differential_evolution
from utils.minimize import minimize

def genetic_algorithm(func: callable, bounds: list[tuple], args: tuple = (), generations: int = 1000, population_size: int = 15, callback: callable = None):
    with GeneticAlgorithm(func,bounds,args,generations,population_size,callback) as genetic_algorithm:
        ret = genetic_algorithm.optimize()
    return ret

class GeneticAlgorithm:
    def __init__(self, func: callable, bounds: list[tuple], args: tuple = (), generations: int = 1000, population_size: int = 15, callback: callable = None):
        self.func: _FunctionWrapper = _FunctionWrapper(func, args)
        self.bounds: list[tuple] = bounds
        self.num_variables: int = len(bounds)

        self.strategy_manager = StrategyManager()
        self.callback = callback

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

            if self.callback:
                best_individual = self.best_individual(self.best_individual)
                best_fitness = self.evaluate_fitness(self.best_individual)
                mutation_rate = self.strategy_manager.get_mutation_rate()
                crossover_rate = self.strategy_manager.get_crossover_rate()

                stop_request = bool(self.callback(generation, best_individual, best_fitness, unique_individuals_count, mutation_rate, crossover_rate))
                if stop_request == True:
                    pass

            if self.evaluate_termination():
                break
        
        res = minimize(self.func, self.best_individual, 'binary_search', self.bounds)
        return res

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
        sorted_population = sorted(paired_population, key=lambda x: x[0], reverse=False)
        return [individual for _, individual in sorted_population]
    
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