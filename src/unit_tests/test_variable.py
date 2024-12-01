import sys
import os

import unittest
import numpy as np
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from diffusiophoresis.variable import Variable

class TestVariable(unittest.TestCase):

    def test_initialization(self):
        """Test that the Variable is initialized with the correct values."""
        var = Variable("TestVar", 10.0, False, 0.0, 20.0)
        self.assertEqual(var.variable_name, "TestVar")
        self.assertEqual(var.value, 10.0)
        self.assertFalse(var.is_constant)
        self.assertEqual(var.min_range, 0.0)
        self.assertEqual(var.max_range, 20.0)

    def test_set_value(self):
        """Test setting the value of a non-constant variable."""
        var = Variable("TestVar", 10.0, False, 0.0, 20.0)
        var.set_value(15.0)
        self.assertEqual(var.value, 15.0)
        
        # Test trying to set value on a constant variable without safe mode
        const_var = Variable("ConstVar", 5.0, True, 0.0, 10.0)
        const_var.set_value(7.0)  # No error, but value should not change
        self.assertEqual(const_var.value, 5.0)

        # Test setting value with safe mode on constant variable
        with self.assertRaises(ValueError):
            const_var.set_value(7.0, safe_mode=True)

    def test_randomize(self):
        """Test that randomize sets a value within range for a non-constant variable."""
        var = Variable("TestVar", 10.0, False, 0.0, 20.0)
        var.randomize()
        self.assertTrue(0.0 <= var.value <= 20.0)

        # Test that randomize doesn't change a constant variable's value
        const_var = Variable("ConstVar", 5.0, True, 0.0, 10.0)
        const_var.randomize()
        self.assertEqual(const_var.value, 5.0)

    def test_is_within_range(self):
        """Test that is_within_range returns the correct result."""
        var = Variable("TestVar", 10.0, False, 0.0, 20.0)
        self.assertTrue(var.is_within_range(10.0))
        self.assertFalse(var.is_within_range(30.0))

    def test_hash_and_equality(self):
        """Test hashing and equality of variables."""
        var1 = Variable("TestVar", 10.0, False, 0.0, 20.0)
        var2 = Variable("TestVar", 10.0, False, 0.0, 20.0)
        var3 = Variable("TestVar", 15.0, False, 0.0, 20.0)

        # Test hash function
        self.assertEqual(hash(var1), hash(var2))
        self.assertNotEqual(hash(var1), hash(var3))

        # Test equality
        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)

    def test_to_dict(self):
        """Test conversion of variable to dictionary."""
        var = Variable("TestVar", 10.0, False, 0.0, 20.0)
        var_dict = var.to_dict()
        self.assertEqual(var_dict['variable_name'], "TestVar")
        self.assertEqual(var_dict['value'], 10.0)
        self.assertFalse(var_dict['is_constant'])
        self.assertEqual(var_dict['min_range'], 0.0)
        self.assertEqual(var_dict['max_range'], 20.0)

    def test_from_dict(self):
        """Test creating a variable from a dictionary."""
        var_data = {
            "variable_name": "TestVar",
            "value": 10.0,
            "is_constant": False,
            "min_range": 0.0,
            "max_range": 20.0
        }
        var = Variable.from_dict(var_data)
        self.assertEqual(var.variable_name, "TestVar")
        self.assertEqual(var.value, 10.0)
        self.assertFalse(var.is_constant)
        self.assertEqual(var.min_range, 0.0)
        self.assertEqual(var.max_range, 20.0)

    def test_str(self):
        """Test the string representation of a variable."""
        var = Variable("TestVar", 10.0, False, 0.0, 20.0)
        self.assertEqual(str(var), "TestVar: 10.0 [0.0, 20.0] (Variable)")
        const_var = Variable("ConstVar", 5.0, True, 0.0, 10.0)
        self.assertEqual(str(const_var), "ConstVar: 5.0 [0.0, 10.0] (Constant)")


if __name__ == '__main__':
    unittest.main()