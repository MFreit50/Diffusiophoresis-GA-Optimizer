import unittest
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from diffusiophoresis.variable import Variable
from diffusiophoresis.variable_definitions import VariableDefinitions
from diffusiophoresis.equation import Equation

class TestEquation(unittest.TestCase):

    def setUp(self):
        # Set up default variables and equation for testing
        VariableDefinitions.variables = {
            "channel_height": Variable(variable_name="channel_height", value=1.0, is_constant=False, min_range=0.5, max_range=2.0),
            "channel_length": Variable(variable_name="channel_length", value=10.0, is_constant=False, min_range=5.0, max_range=20.0),
            "mean_velocity": Variable(variable_name="mean_velocity", value=1.0, is_constant=False, min_range=0.1, max_range=5.0),
            "diffusiophoretic_velocity": Variable(variable_name="diffusiophoretic_velocity", value=0.1, is_constant=False, min_range=0.01, max_range=0.5),
            "beta_potential": Variable(variable_name="beta_potential", value=25.0, is_constant=False, min_range=10.0, max_range=50.0),
            "cation": Variable(variable_name="cation", value=1.0, is_constant=False, min_range=0.1, max_range=2.0),
            "anion": Variable(variable_name="anion", value=1.0, is_constant=False, min_range=0.1, max_range=2.0),
            "electrophoretic_mobility": Variable(variable_name="electrophoretic_mobility", value=0.001, is_constant=False, min_range=0.0001, max_range=0.01),
            "chemiphoretic_mobility": Variable(variable_name="chemiphoretic_mobility", value=0.001, is_constant=False, min_range=0.0001, max_range=0.01),
            "chemiphoretic_gradient": Variable(variable_name="chemiphoretic_gradient", value=0.01, is_constant=False, min_range=0.001, max_range=0.1),
            "valence_charge": Variable(variable_name="valence_charge", value=1.0, is_constant=False, min_range=0.1, max_range=3.0),
            "elementary_charge": Variable(variable_name="elementary_charge", value=1.6e-19, is_constant=True,min_range=0.1, max_range=3.0),
            "zeta_potential": Variable(variable_name="zeta_potential", value=0.02, is_constant=False, min_range=0.01, max_range=0.05),
            "absolute_temperature": Variable(variable_name="absolute_temperature", value=298.15, is_constant=False, min_range=273.15, max_range=373.15),
            "fluid_density": Variable(variable_name="fluid_density", value=1000.0, is_constant=True, min_range=900.0, max_range=1200.0),
            "fluid_velocity": Variable(variable_name="fluid_velocity", value=1.0, is_constant=False, min_range=0.1, max_range=5.0),
            "dynamic_viscosity": Variable(variable_name="dynamic_viscosity", value=0.001, is_constant=False, min_range=0.0005, max_range=0.002),
            "ci": Variable(variable_name="ci", value=1.0, is_constant=False, min_range=0.1, max_range=10.0),
            "cb": Variable(variable_name="cb", value=1.0, is_constant=False, min_range=0.1, max_range=10.0),
            "length": Variable(variable_name="length", value=10.0, is_constant=False, min_range=5.0, max_range=20.0),
            "characteristic_length": Variable(variable_name="characteristic_length", value=2.0, is_constant=False, min_range=1.0, max_range=5.0),
            "exclusion_zone_area": Variable(variable_name="exclusion_zone_area", value=5.0, is_constant=False, min_range=1.0, max_range=10.0)
        }
        self.equation = Equation()

    def test_add_variable(self):
        # Test adding a new variable
        new_variable = Variable("new_variable", 5.0, False, 0.0, 10.0)
        self.equation.add_variable(new_variable)
        self.assertTrue(self.equation.has_variable("new_variable"))
        self.assertEqual(self.equation.get_value("new_variable"), 5.0)

    def test_get_variable(self):
        # Test retrieving an existing variable
        variable = self.equation.get_variable("channel_height")
        self.assertEqual(variable.value, 1.0)

    def test_set_value(self):
        # Test setting the value of a variable
        self.equation.set_value("channel_length", 12.0, True)
        self.assertEqual(self.equation.get_value("channel_length"), 12.0)

        # Test attempting to set a constant variable
        with self.assertRaises(ValueError):
            self.equation.set_value("fluid_density", 1100.0, True)

    def test_randomize_equation(self):
        # Test randomizing all non-constant variables in the equation
        old_values = {name: var.value for name, var in self.equation.variables.items() if not var.is_constant}
        self.equation.randomize_equation()
        new_values = {name: var.value for name, var in self.equation.variables.items() if not var.is_constant}

        for name in old_values:
            self.assertNotEqual(old_values[name], new_values[name])

    def test_get_index(self):
        # Test retrieving a variable by index
        variable = self.equation.get_index(1)
        self.assertEqual(variable.variable_name, "channel_length")

        # Test for out-of-range index
        with self.assertRaises(IndexError):
            self.equation.get_index(50)

    def test_equality_and_hash(self):
        # Test that two equations with the same variables are considered equal
        eq2 = Equation()
        self.assertEqual(self.equation, eq2)
        self.assertEqual(hash(self.equation), hash(eq2))

        # Test inequality after modifying a variable in one of the equations
        eq2.set_value("channel_length", 14.0)
        self.assertNotEqual(self.equation, eq2)

    def test_get_exclusion_zone_area(self):
        # Test the exclusion zone area calculation (dummy test)
        area = self.equation.get_exlcusion_zone_area()
        self.assertIsNotNone(area)  # Assume there's a valid calculation

if __name__ == "__main__":
    unittest.main()