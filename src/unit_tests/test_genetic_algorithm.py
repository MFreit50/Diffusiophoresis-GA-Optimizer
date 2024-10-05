import random
import sys
import os
import unittest
from unittest.mock import MagicMock, patch
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from diffusiophoresis.equation import Equation
from genetic_algorithm import GeneticAlgorithm

class TestGeneticAlgorithm(unittest.TestCase):
    
    def setUp(self):
        # Setup the GeneticAlgorithm with reasonable defaults
        self.generations = 10
        self.population_size = 10
        self.crossover_rate = 0.8
        self.mutation_rate = 0.1
        self.ga = GeneticAlgorithm(self.generations, self.population_size, self.crossover_rate, self.mutation_rate)

    @patch('diffusiophoresis.equation.Equation')
    def test_initialize_population(self, MockEquation):
        # Mock the randomize_equation method to return a dummy equation
        equation_instance = MockEquation.return_value
        equation_instance.randomize_equation.return_value = equation_instance
        
        self.ga.initialize_population()
        
        self.assertEqual(len(self.ga.population), self.population_size)
        MockEquation.assert_called()
        equation_instance.randomize_equation.assert_called()

    @patch('diffusiophoresis.equation.Equation')
    def test_select_parents(self, MockEquation):
        # Mocking individuals in the population
        equation_instance = MockEquation.return_value
        self.ga.population = [equation_instance for _ in range(self.population_size)]
        
        # Mocking fitness evaluation
        self.ga.evaluate_fitness = MagicMock(side_effect=lambda eq: random.uniform(0, 1))
        
        parent1, parent2 = self.ga.select_parents()
        
        self.assertIsNotNone(parent1)
        self.assertIsNotNone(parent2)
        self.assertNotEqual(parent1, parent2)
        self.ga.evaluate_fitness.assert_called()

    @patch('diffusiophoresis.equation.Equation')
    def test_mutation_adjustment(self, MockEquation):
        equation_instance = MockEquation.return_value
        self.ga.population = [equation_instance for _ in range(self.population_size)]
        
        # Mock evaluate_fitness to return low diversity
        self.ga.evaluate_population_fitness = MagicMock(return_value=[1.0 for _ in range(self.population_size)])

        self.ga.evolve()
        
        # Check mutation rate adjustment based on population diversity
        self.assertGreaterEqual(self.ga.mutation_rate, 0.1)

    @patch('diffusiophoresis.equation.Equation')
    def test_crossover(self, MockEquation):
        # Mock two parent equations
        parent1 = MockEquation()
        parent2 = MockEquation()
        
        # Test crossover function
        child1, child2 = self.ga.crossover(parent1, parent2)
        
        self.assertIsNotNone(child1)
        self.assertIsNotNone(child2)

    @patch('diffusiophoresis.equation.Equation')
    def test_evaluate_population_fitness(self, MockEquation):
        # Mocking the equations and their fitness evaluation
        equation_instance = MockEquation.return_value
        self.ga.population = [equation_instance for _ in range(self.population_size)]
        
        with patch.object(self.ga, 'evaluate_fitness', return_value=10.0):
            fitness_scores = self.ga.evaluate_population_fitness(self.ga.population)
        
        self.assertEqual(len(fitness_scores), self.population_size)
        self.assertTrue(all(score == 10.0 for score in fitness_scores))

    @patch('diffusiophoresis.equation.Equation')
    def test_run(self, MockEquation):
        equation_instance = MockEquation.return_value
        equation_instance.randomize_equation.return_value = equation_instance
        equation_instance.optimize.return_value = 10.0
        
        # Mock population fitness and crossover/mutation behavior
        self.ga.initialize_population = MagicMock()
        self.ga.evolve = MagicMock()

        best_equation = self.ga.run()
        
        self.ga.initialize_population.assert_called()
        self.ga.evolve.assert_called()
        self.assertEqual(best_equation, self.ga.best_equation)

if __name__ == '__main__':
    unittest.main()