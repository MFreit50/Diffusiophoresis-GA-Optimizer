import copy
import random

import numpy as np
from diffusiophoresis.equation import Equation
from abc import ABC, abstractmethod

class SelectionStrategy(ABC):
    @abstractmethod
    def select_parents(self, population, fitness_scores, optimize_mode) -> tuple[Equation, Equation]:
        pass

class TournamentSelection(SelectionStrategy):
    def select_parents(self, population, fitness_scores, optimize_mode) -> tuple[Equation, Equation]:
        tournament_size = 6
        parent1, parent2 = self.tournament_selection(population, fitness_scores, tournament_size, optimize_mode)
        parent1 = copy.deepcopy(parent1)
        parent2 = copy.deepcopy(parent2)
        return parent1, parent2

    def tournament_selection(self, population: list, fitness_scores: list, tournament_size: int, optimize_mode: bool) -> list:
        def tournament_select_parent():
            tournament_contestants_indices = random.sample(range(len(population)), tournament_size)

            if optimize_mode == True: # Maximize
                best_contestant_index = max(tournament_contestants_indices, key=lambda idx: fitness_scores[idx])
            else:   # Minimize
                best_contestant_index = min(tournament_contestants_indices, key=lambda idx: fitness_scores[idx])

            return population[best_contestant_index]
        
        parent1 = tournament_select_parent()
        parent2 = tournament_select_parent()
        '''
        while parent1 == parent2:
            parent2 = tournament_select_parent()
        '''
        return parent1, parent2

class RouletteSelection(SelectionStrategy):
    def select_parents(self, population, fitness_scores, optimize_mode) -> tuple[Equation, Equation]:
        parent1, parent2 = self.roulette_selection(population, fitness_scores, optimize_mode)
        parent1 = copy.deepcopy(parent1)
        parent2 = copy.deepcopy(parent2)
        return parent1, parent2

    def roulette_selection(self, population, fitness_scores, maximize=True) -> tuple[list, list]:
        """
        Perform roulette wheel selection with handling for zero or uniform fitness scores.
        
        :param population: List of individuals in the population.
        :param fitness_scores: List of fitness scores corresponding to the population.
        :param maximize: Boolean indicating if the GA is maximizing or minimizing.
        :return: Two selected parents.
        """
        epsilon = 1e-10  # Small constant to avoid division by zero

        if not maximize:
            # Invert fitness scores for minimization
            max_fitness = max(fitness_scores)
            fitness_scores = [max_fitness - fitness for fitness in fitness_scores]
        
        # Handle the case of zero or uniform fitness scores
        total_fitness = sum(fitness_scores)
        if total_fitness <= epsilon:
            # Fall back to random selection if all scores are the same
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            return parent1, parent2

        # Step 1: Calculate cumulative probabilities
        cumulative_probabilities = []
        cumulative_sum = 0
        for fitness in fitness_scores:
            normalized_probability = fitness / total_fitness
            cumulative_sum += normalized_probability
            cumulative_probabilities.append(cumulative_sum)

        # Step 2: Select individual randomly
        def roulette_select_parent():
            random_value = random.random()
            for i, cumulative_probability in enumerate(cumulative_probabilities):
                if random_value <= cumulative_probability:
                    return population[i]

        parent1 = roulette_select_parent()
        parent2 = roulette_select_parent()

        return parent1, parent2
            
