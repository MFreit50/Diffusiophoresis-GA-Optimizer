import math
import numpy as np
from ga.genetic_algorithm import genetic_algorithm
from interfaces.test_function import TestFunction
import time
import json
import os

class GeneticAlgorithmBenchmark:
    def __init__(self, generations = 1000, population_size = 15, function_list = None, iterations = 1000, report_file="benchmark_report.json"):
        """
        Initialize the benchmark class with a list of test functions and the number of iterations.
        """
        self.generations = generations
        self.population_size = population_size
        self.function_list = function_list
        self.iterations = iterations
        self.report_file = report_file
        self._report = {}

    def save_report_to_file(self):
        """
        Save the benchmark report to a JSON file. If the file exists, append new results.
        """
        # Load existing report if file exists
        if os.path.exists(self.report_file):
            with open(self.report_file, 'r') as file:
                existing_data = json.load(file)
        else:
            existing_data = {}

        # Merge current report with existing data
        existing_data.update(self._report)

        # Save merged data back to the file
        with open(self.report_file, 'w') as file:
            json.dump(existing_data, file, indent=4)

        print(f"Report saved to {self.report_file}")

    def benchmark_ga(self, ga_result, optimal_solution, tolerance=0.01):
        """
        Calculate benchmark metrics for the genetic algorithm's output.
        """
        ga_result = np.array(ga_result)
        optimal_solution = np.array(optimal_solution)
        absolute_errors = np.abs(ga_result - optimal_solution)
        
        mae = np.mean(absolute_errors)
        mre = np.mean(absolute_errors / np.abs(optimal_solution))
        rmse = np.sqrt(np.mean((ga_result - optimal_solution) ** 2))
        max_error = np.max(absolute_errors)
        percent_match = np.mean(absolute_errors <= tolerance) * 100
        
        return {
            "Mean Absolute Error": mae,
            "Mean Relative Error": mre,
            "Root Mean Square Error": rmse,
            "Maximum Error": max_error,
            "Percent Match": percent_match,
        }

    def calculate_max_possible_errors(self, bounds):
        """
        Calculate maximum possible distance and function errors based on the problem bounds.
        """
        max_distance = math.sqrt(sum((b - a)**2 for a, b in bounds))
        bound_array = np.array(bounds)
        max_function_error = np.linalg.norm(bound_array[:, 1] - bound_array[:, 0])
        return max_distance, max_function_error

    def evaluate_function(self, func, bounds, args, solution):
        """
        Run the genetic algorithm multiple times for a given function and collect metrics.
        """
        distance_errors = []
        function_errors = []
        execution_times = []
        benchmark_metrics = []
        all_results = []

        for i in range(self.iterations):
            print(f"Iteration: {i + 1}")
            start_time = time.time()
            result = self.run_genetic_algorithm(func, bounds, args)
            end_time = time.time()
            
            # Store the result
            all_results.append(result)

            # Calculate errors
            distance_error = np.linalg.norm(np.array(result) - np.array(solution))
            function_error = abs(func(result, args) - func(solution, args))
            
            # Record metrics
            distance_errors.append(distance_error)
            function_errors.append(function_error)
            execution_times.append(end_time - start_time)
            benchmarks = self.benchmark_ga(result, solution)
            benchmark_metrics.append(benchmarks)
        
        return distance_errors, function_errors, execution_times, benchmark_metrics, all_results

    def run_genetic_algorithm(self, func, bounds, args):
        """
        Placeholder for the genetic algorithm call.
        Replace this with the actual genetic algorithm implementation.
        """
        return genetic_algorithm(func, bounds, args, self.generations, self.population_size)

    def aggregate_results(self, distance_errors, function_errors, execution_times, benchmark_metrics, max_distance, max_function_error, all_results):
        """
        Aggregate results from all iterations to compute averages and overall accuracy.
        """
        avg_distance_error = np.mean(distance_errors)
        avg_function_error = np.mean(function_errors)
        avg_time = np.mean(execution_times)

        # Aggregate additional benchmarks
        avg_benchmarks = {key: np.mean([bm[key] for bm in benchmark_metrics]) for key in benchmark_metrics[0]}
        
        # Calculate overall accuracy
        normalized_distance_error = avg_distance_error / max_distance if max_distance > 0 else 0
        normalized_function_error = avg_function_error / max_function_error if max_function_error > 0 else 0
        overall_accuracy = 0.5 * (normalized_distance_error + normalized_function_error)

        # Calculate average result
        avg_result = np.mean(all_results, axis=0)

        return {
            'avg_distance_error': avg_distance_error,
            'avg_function_error': avg_function_error,
            'avg_time': avg_time,
            'overall_accuracy': overall_accuracy,
            'avg_result': avg_result.tolist(),  # Convert to list for JSON-compatibility if needed
            **avg_benchmarks,
            'distance_errors': distance_errors,
            'function_errors': function_errors,
            'execution_times': execution_times,
            'results': all_results
        }
    
    def run(self):
        """
        Run the benchmark for each function in the list and store results in the report.
        """
        for test_func in self.function_list:
            func_name = test_func.__name__ if hasattr(test_func, '__name__') else str(test_func)
            print(f'Function: {func_name}')
            
            # Retrieve function parameters and solution
            func, bounds, args = test_func.get_parameters()
            solution = test_func.solution()
            
            # Precompute maximum errors for normalization
            max_distance, max_function_error = self.calculate_max_possible_errors(bounds)
            
            # Evaluate the function
            distance_errors, function_errors, execution_times, benchmark_metrics, all_results = self.evaluate_function(
                func, bounds, args, solution
            )
            
            # Aggregate results
            self._report[f'Function {func_name}'] = self.aggregate_results(
                distance_errors, function_errors, execution_times, benchmark_metrics, max_distance, max_function_error, all_results
            )

        # Print the full report
        self.print_report()

    def print_report(self):
        """
        Print the benchmark results in a structured format.
        """
        print("Benchmark Report:")
        for func_name, metrics in self._report.items():
            print(f"\n{func_name}:")
            for metric, value in metrics.items():
                if isinstance(value, list) and len(value) > 10:  # Avoid printing large lists
                    continue
                print(f"  {metric}: {value}")
            print()
        self.save_report_to_file()