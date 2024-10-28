import copy
import statistics
import time
import psutil
from diffusiophoresis.equation import Equation

class ProgressAnalyzer():
    def __init__(self):
        self.best_individual : Equation = None
        self.previous_best_individual : Equation = None

        self.best_individual_fitness : float = None
        self.previous_best_individual_fitness : float = None

        self.no_improvement_counter: int = 0

        self.fitness_improvement = 0
        self.unique_individuals_count = 0

        self.generation_start_time = time.time()
        self.generation_end_time = time.time()
        self.start_time = time.time()
        self.process = psutil.Process()
    
    def analyze(self, population, fitness_scores):
        sorted_population, sorted_fitness_scores = self.sort_population_by_fitness(population, fitness_scores)

        # Update Best Individual
        self.previous_best_individual = copy.deepcopy(self.best_individual)
        self.previous_best_individual_fitness = copy.deepcopy(self.best_individual_fitness)
        self.best_individual = sorted_population[0]
        self.best_individual_fitness = sorted_fitness_scores[0]

        # Calculate Progress Stagnance
        if self.previous_best_individual_fitness is not None:
            if self.previous_best_individual_fitness == self.best_individual_fitness:
                self.no_improvement_counter += 1
            else:
                self.no_improvement_counter = 0

        # Calculate Statistics
        average_population_fitness = sum(fitness_scores) / len(fitness_scores)
        mean_population_fitness = statistics.mean(fitness_scores)
        median_population_fitness = statistics.median(fitness_scores)
        standard_deviation = statistics.stdev(fitness_scores) if len(fitness_scores) > 1 else 0
        fitness_range = sorted_fitness_scores[0] - sorted_fitness_scores[-1]

        # Track Unique Individuals
        unique_individuals = set(population)
        self.unique_individuals_count = len(unique_individuals)
        self.unique_individuals_percentage = self.unique_individuals_count / len(population)

        # Calculate Improvement and Mutation Rate
        if self.previous_best_individual is not None:
            fitness_improvement = self._calculate_fitness_improvement()
        else:
            fitness_improvement = None

        # Track Time
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        generation_end_time = current_time - self.generation_start_time
        self.generation_start_time = current_time

        #Track Memory Usage
        memory_mb = self.process.memory_info().rss / (1024 ** 2)

        # Aggregate Data into a Dictionary
        data = {
            "average_fitness": average_population_fitness,
            "mean_fitness": mean_population_fitness,
            "median_fitness": median_population_fitness,
            "standard_deviation": standard_deviation,
            "fitness_range": fitness_range,
            "unique_individuals_count": self.unique_individuals_count,
            "unique_individuals_percentage": self.unique_individuals_percentage,
            "fitness_improvement": fitness_improvement,
            "elapsed_time": elapsed_time,
            "generation_end_time": generation_end_time,
            "memory_usage_MB": memory_mb,
            "no_improvement_counter": self.no_improvement_counter
        }

        return data
    
    def sort_population_by_fitness(self, population, fitness_scores):
            """
            Returns a new population sorted by their fitness scores in descending order.
            """
            paired_population = list(zip(fitness_scores, population))
            sorted_population = sorted(paired_population, key=lambda x: x[0], reverse=True)

            sorted_fitness_scores = [fitness for _, fitness in sorted_population]
            sorted_individuals = [individual for individual, _ in sorted_population]

            return sorted_fitness_scores, sorted_individuals

    def _calculate_fitness_improvement(self):
        return (((self.best_individual_fitness) - (self.previous_best_individual_fitness)) / abs(self.previous_best_individual_fitness)) * 100