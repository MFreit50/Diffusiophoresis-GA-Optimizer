import copy
import random

class Selection():
    def select_parents(self, population, fitness_scores) -> tuple:
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

        if(method == "tournament"):
            parent1, parent2 = self.tournament_selection(population, fitness_scores, tournament_size=6)
        elif(method == "roulette"):
            parent1, parent2 = self.roulette_selection(population, fitness_scores)
        else:
            raise NotImplementedError("This selection method is either invalid or not implemented yet!")

        parent1 = copy.deepcopy(parent1)
        parent2 = copy.deepcopy(parent2)
        return parent1, parent2

    def roulette_selection(self, population, fitness_scores):
        #Step 1: calculate total fitness
        total_fitness: float = sum(fitness for fitness in fitness_scores)

        #Step 2: calculate cummulative probabilities
        cummulative_probabilities: list = []
        cummulative_sum: float = 0
        for fitness in fitness_scores:
            normalized_probability: float = fitness / total_fitness
            cummulative_sum += normalized_probability
            cummulative_probabilities.append(cummulative_sum)

        #Step 3: select individual randomly
        def roulette_select_parent():
            random_value = random.random()
            for i, cummulative_probability in enumerate(cummulative_probabilities):
                if random_value <= cummulative_probability:
                    return population[i]
        
        parent1 = roulette_select_parent()
        parent2 = roulette_select_parent()

        return parent1, parent2
            
    def tournament_selection(self, population: list, fitness_scores: list, tournament_size: int) -> tuple:
        """
        Perform tournament selection to choose top individuals from a population

        Args:
            tournament_size: The number of individuals participating in the tournament

        Returns: tuple: A tuple containing the selected individuals
        """
        def tournament_select_parent():
            tournament_contestants_indices = random.sample(range(len(population)), tournament_size)
            best_contestant_index = max(tournament_contestants_indices, key=lambda idx: fitness_scores[idx])
            return population[best_contestant_index]
        
        parent1 = tournament_select_parent()
        parent2 = tournament_select_parent()
        while parent1 == parent2:
            parent2 = tournament_select_parent()
            
        return parent1, parent2