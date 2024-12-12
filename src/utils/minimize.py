import copy


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
        #print(f"Step Size: {step_size}")
        return step_size

def _hill_climb(func, individual: list, max_iterations: int = 100) -> list:
        """
        Perform hill climbing to optimize the given equation.

        Args:
            max_iterations (int): Maximum number of iterations for hill climbing.
            step_size (float): The step size to explore neighboring solutions.

        Returns:
            Equation: The optimized equation after hill climbing.
        """
        current_individual = copy.deepcopy(individual)
        current_fitness = func(individual)
        
        for iteration in range(max_iterations):
            #print(f"Iteration: {iteration}")
            improved = False
            
            # Loop through each variable to optimize it
            for i in range(len(individual)):
                var = individual[i]
                best_value = var  # Track the best value for this variable
                
                step_size = get_msd_step_size(var)  # Get the most significant digit after the decimal point
                
                # Try moving the variable up and down by step_size
                for delta in [-step_size, step_size]:
                    #print(f"Trying delta: {delta}")
                    #print(f"Original Value: {var}")
                    var += delta
                    #print(f"New Value: {var}")
                    individual[i] = var
                    new_fitness = func(individual)
                    
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

def _binary_search(func, individual : list, bounds) -> list:
        def bs(low, middle, high, individual: list, gene_index: int) -> list:
            def evaluate(individual: list, gene_index: int, value : float) -> float:
                individual[gene_index] = value
                return func(individual)
            
            if low == middle or high == middle:
                individual[gene_index] = middle
                return individual
            
            new_low = (middle+low)/2
            new_high = (middle+high)/2
            
            new_low_score = evaluate(individual, gene_index, new_low)
            new_high_score = evaluate(individual, gene_index, new_high)

            if new_low_score < new_high_score:
                return bs(low, new_low, middle, individual, gene_index)
            else:
                return bs(middle, new_high, high, individual, gene_index)
        individual = copy.deepcopy(individual)

        for i in range(len(individual)):
            min, max = bounds[i]
            middle = individual[i]
            low = middle - 0.1 if min < middle - 0.1 < max else middle
            high= middle + 0.1 if min < middle + 0.1 < max else middle
            individual = bs(low, middle, high, individual, i)

        return individual

def minimize(func, x0, method=None, bounds=None):
    if method == None:
        return _binary_search(func, x0, bounds)
    if method == 'binary_search':
        return _binary_search(func, x0, bounds)
    if method == 'hill_climb':
        return _hill_climb(func, x0, 100)