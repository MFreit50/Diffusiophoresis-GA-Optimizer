import numpy as np

# Define Rastrigin function
def rastrigin(x):
    A = 10
    return A * len(x) + sum([(xi ** 2 - A * np.cos(2 * np.pi * xi)) for xi in x])

# Genetic Algorithm Parameters
POPULATION_SIZE = 2000
DIMENSIONS = 2  # Number of variables
GENERATIONS = 10000
MUTATION_RATE = 0.05
CROSSOVER_RATE = 0.9
BOUND_LOW, BOUND_HIGH = -5.12, 5.12  # Typical bounds for Rastrigin

# Initialize Population
def initialize_population():
    return np.random.uniform(BOUND_LOW, BOUND_HIGH, (POPULATION_SIZE, DIMENSIONS))

# Evaluate Fitness
def evaluate_population(population):
    return np.array([rastrigin(individual) for individual in population])

# Selection (Tournament Selection)
def select_parents(population, fitness):
    parents = []
    for _ in range(POPULATION_SIZE):
        i, j = np.random.randint(0, POPULATION_SIZE, 2)
        if fitness[i] < fitness[j]:
            parents.append(population[i])
        else:
            parents.append(population[j])
    return np.array(parents)

# Crossover (Uniform Crossover)
def crossover(parent1, parent2):
    if np.random.rand() < CROSSOVER_RATE:
        mask = np.random.rand(DIMENSIONS) > 0.5
        child1 = np.where(mask, parent1, parent2)
        child2 = np.where(mask, parent2, parent1)
        return child1, child2
    return parent1, parent2

# Mutation
def mutate(individual):
    for i in range(DIMENSIONS):
        if np.random.rand() < MUTATION_RATE:
            individual[i] = np.random.uniform(BOUND_LOW, BOUND_HIGH)
    return individual

# Genetic Algorithm Execution
def genetic_algorithm():
    population = initialize_population()
    best_solution = None
    best_fitness = float('inf')

    for generation in range(GENERATIONS):
        fitness = evaluate_population(population)

        # Track the best solution
        current_best_idx = np.argmin(fitness)
        current_best_fitness = fitness[current_best_idx]
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_solution = population[current_best_idx]

        print(f"Generation {generation}, Best Fitness: {best_fitness}")

        # Selection
        parents = select_parents(population, fitness)

        # Crossover and Mutation
        next_generation = []
        for i in range(0, POPULATION_SIZE - 2, 2):  # Leave room for two elites
            parent1, parent2 = parents[i], parents[i + 1]
            child1, child2 = crossover(parent1, parent2)
            next_generation.append(mutate(child1))
            next_generation.append(mutate(child2))

        # Adding the two best individuals to the next generation (elitism)
        next_generation.append(population[current_best_idx])
        next_generation.append(population[np.argsort(fitness)[1]])

        population = np.array(next_generation)

    return best_solution, best_fitness

# Run the Genetic Algorithm
best_solution, best_fitness = genetic_algorithm()
print("Best Solution:", best_solution)
print("Best Fitness:", best_fitness)