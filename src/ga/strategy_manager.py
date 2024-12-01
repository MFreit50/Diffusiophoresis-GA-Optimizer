from ga.mutation_strategy import *
from ga.crossover_strategy import *
from ga.selection_strategy import *

'''
    StrategyManager class is responsible for managing the mutation, crossover, and selection strategies.
    It is responsible for picking the strategies to be used in the genetic algorithm.
'''
class StrategyManager():
    def __init__(self):
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
        
        self.mutation_rate: float = 0.01
        self.crossover_rate: float = 0.07

        self.mutation_strategy: MutationStrategy = None
        self.crossover_strategy: CrossoverStrategy = None
        self.selection_strategy: SelectionStrategy = None   
        
        self.update_strategies(0, [], 0)     
        
    def update_strategies(self, diversity_score: float, fitness_scores: list, population_size: int):
        
        if diversity_score < population_size * 0.65:  # Low diversity
            self.mutation_rate = min(self.mutation_rate * 1.1, 0.95)
            pass
        else:
            self.mutation_rate = max(self.mutation_rate * 0.9, 0.01)
            pass
        
        self.crossover_strategy = self.pick_crossover_strategy()
        self.selection_strategy = self.pick_selection_strategy()
        self.mutation_strategy = self.pick_mutation_strategy()
    
    def pick_mutation_strategy(self) -> MutationStrategy:
        # List of strategies and corresponding weights
        strategies: list[str] = ["randomize", "step", "step", "step"]
        choice: str = random.choice(strategies)
        choice: MutationStrategy = self.available_mutation_strategies[choice]
        return choice
    
    def pick_crossover_strategy(self) -> CrossoverStrategy:
        choice: CrossoverStrategy = random.choice(list(self.available_crossover_strategies.values()))
        return choice
    
    def pick_selection_strategy(self) -> SelectionStrategy:
        choice: SelectionStrategy = random.choice(list(self.available_selection_strategies.values()))
        return choice   
        
    def mutate(self, population: Equation) -> Equation:
        mutated_population = []

        for individual in population:
            if np.random.rand() > self.mutation_rate:
                mutated_population.append(individual)
            else:
                self.mutation_strategy = self.pick_mutation_strategy()
                mutated_individual = self.mutation_strategy.mutate(individual)
                mutated_population.append(mutated_individual)

        return mutated_population

    def crossover(self, selected_parents : list) -> tuple[Equation, Equation]:
        offspring = []

        for parent1, parent2 in selected_parents:
            if np.random.rand() > self.crossover_rate:
                offspring.extend([parent1, parent2])
            else:
                self.crossover_strategy = self.pick_crossover_strategy()
                child1, child2 = self.crossover_strategy.crossover(parent1, parent2)
                offspring.extend([child1, child2])
        
        return offspring
    
    def select_parents(self, population: list[Equation], fitness_scores: list) -> tuple[Equation, Equation]:
        selected_population = []

        while len(selected_population)*2 < len(population):
            self.selection_strategy = self.pick_selection_strategy()
            parent1, parent2 = self.selection_strategy.select_parents(population, fitness_scores)
            selected_population.append((parent1, parent2))

        return selected_population
    
    def get_mutation_rate(self) -> float:
        return self.mutation_rate
    
    def get_crossover_rate(self) -> float:
        return self.crossover_rate