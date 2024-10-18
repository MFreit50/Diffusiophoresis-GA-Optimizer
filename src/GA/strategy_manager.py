from GA.mutation_strategy import *
from GA.crossover_strategy import *
from GA.selection_strategy import *

'''
    StrategyManager class is responsible for managing the mutation, crossover, and selection strategies.
    It is responsible for picking the strategies to be used in the genetic algorithm.
'''
class StrategyManager:
    def __init__(self, mutation_rate: float, crossover_rate: float):
        self.available_mutation_strategies = {
            "randomize": RandomizeMutation(),
            "step": StepMutation()
        }
        self.available_crossover_strategies = {
            "single_point": SinglePointCrossover(),
            "uniform": UniformCrossover()
        }
        self.available_selection_strategies = {
            "roulette_wheel": RouletteSelection(),
            "tournament": TournamentSelection()
        }
        
        self.mutation_rate: float = mutation_rate
        self.crossover_rate: float = crossover_rate

        self.mutation_strategy: MutationStrategy = None
        self.crossover_strategy: CrossoverStrategy = None
        self.selection_strategy: SelectionStrategy = None   
           
    def pick_mutation_strategy(self) -> MutationStrategy:
        # List of strategies and corresponding weights
        strategies: list[str] = ["randomize", "step", "step", "step"]
        choice: str = random.choice(strategies)
        choice: MutationStrategy = self.available_mutation_strategies[choice]
        self.mutation_strategy = choice
    
    def pick_crossover_strategy(self) -> CrossoverStrategy:
        choice: CrossoverStrategy = random.choice(list(self.available_crossover_strategies.values()))
        self.crossover_strategy = choice
    
    def pick_selection_strategy(self) -> SelectionStrategy:
        choice: SelectionStrategy = random.choice(list(self.available_selection_strategies.values()))
        self.selection_strategy = choice 
        
    def mutate(self, child: Equation) -> Equation:
        self.pick_mutation_strategy()
        if np.random.rand() > self.mutation_rate:
            return child
        return self.mutation_strategy.mutate(child)

    def crossover(self, parent1: Equation, parent2: Equation) -> tuple[Equation, Equation]:
        self.pick_crossover_strategy()
        if np.random.rand() > self.crossover_rate:
            return parent1, parent2
        return self.crossover_strategy.crossover(parent1, parent2)
    
    def select_parents(self, population: list[Equation], fitness_scores: list) -> tuple[Equation, Equation]:
        self.pick_selection_strategy()
        return self.selection_strategy.select_parents(population, fitness_scores)
    
    def update_mutation_rate_by_fitness(self, best_fitness: Equation, previous_best_fitness: float):
        # Adjust mutation rate based on fitness improvement
        if previous_best_fitness:
            # Calculate the percentage improvement in fitness
            fitness_improvement: float = ((best_fitness 
                                        - previous_best_fitness) 
                                        / abs(previous_best_fitness)) * 100

            if fitness_improvement < 10:  # No significant improvement
                self.mutation_rate = min(self.mutation_rate * 1.2, 0.5)  # Increase mutation rate
            else:
                self.mutation_rate = max(self.mutation_rate * 0.8, 0.01)  # Decrease mutation rate    
    
    def update_mutation_rate_by_diversity(self, diversity_score: float, population_size: int):
        if diversity_score < 0.5:  # Low diversity
            self.mutation_rate = min(self.mutation_rate * 1.1, 0.5)
            pass
        else:
            self.mutation_rate = max(self.mutation_rate * 0.9, 0.01)
            pass  
        
    def get_mutation_rate(self) -> float:
        return self.mutation_rate
    
    def get_crossover_rate(self) -> float:
        return self.crossover_rate