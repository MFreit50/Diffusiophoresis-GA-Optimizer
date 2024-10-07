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
        #print("method: ", method)
        parent1 = None
        parent2 = None
        if(method == "tournament"):
            parent1, parent2 = self.tournament_selection(population, tournament_size=6)
        elif(method == "roulette"):
            parent1, parent2 = self.roulette_selection(population, fitness_scores)
        else:
            raise NotImplementedError("This selection method is either invalid or not implemented yet!")

        return parent1, parent2

    def roulette_selection(self, population, fitness_scores):
        #Step 1: calculate total fitness
        total_fitness: float = sum(fitness for fitness in fitness_scores)

        #Step 2: calculate cummulative probabilities
        cummulative_probabilities: list = []
        cummulative_sum: float = 0
        for fitness in self.fitness_scores:
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
            
    def tournament_selection(self, population: list, tournament_size: int) -> tuple:
        """
        Perform tournament selection to choose top individuals from a population

        Args:
            tournament_size: The number of individuals participating in the tournament

        Returns: tuple: A tuple containing the selected individuals
        """
        
        # First tournament
        tournament_contestants1 = random.sample(population, tournament_size)
        parent1 = max(tournament_contestants1, key=lambda individual: self.evaluate_fitness(individual))

        #Remove the first parent from the population
        population_without_parent1 = [individual for individual in population if individual != parent1]

        #Second tournament
        tournament_contestants2 = random.sample(population_without_parent1, tournament_size)
        parent2 = max(tournament_contestants2, key=lambda individual: self.evaluate_fitness(individual))

        return parent1, parent2