import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from diffusiophoresis.variable import Variable

class VariableEntry(ttk.Frame):
    def __init__(self, parent, variable_name, min_range=0.0, max_range=100.0):
        super().__init__(parent)

        self.variable_name = variable_name
        self.var_value = tk.DoubleVar()
        self.var_is_constant = tk.BooleanVar()

        # Label for variable name
        ttk.Label(self, text=variable_name).grid(row=0, column=0, sticky='e', padx=10)

        # Entry for variable value (slightly larger width)
        self.entry = ttk.Entry(self, textvariable=self.var_value, width=15)
        self.entry.grid(row=0, column=1, padx=5)

        # Min and Max Range Entry (positioned further to the right with more width)
        self.min_range = min_range  # Store min and max directly from the constructor
        self.max_range = max_range
        self.min_range_var = tk.DoubleVar(value=min_range)
        self.max_range_var = tk.DoubleVar(value=max_range)
        self.min_entry = ttk.Entry(self, textvariable=self.min_range_var, width=10)
        self.max_entry = ttk.Entry(self, textvariable=self.max_range_var, width=10)
        self.min_entry.grid(row=0, column=2, padx=(10, 5))  # Padded to the right
        ttk.Label(self, text="to").grid(row=0, column=3, padx=5)
        self.max_entry.grid(row=0, column=4, padx=5)

        # Checkbox for constant
        self.constant_checkbox = ttk.Checkbutton(self, text="Constant", variable=self.var_is_constant)
        self.constant_checkbox.grid(row=0, column=5, padx=10)

    def get_value(self):
        try:
            value = self.var_value.get()  # Get the value from entry
            min_range = float(self.min_range_var.get())  # Make sure it's cast to float
            max_range = float(self.max_range_var.get())

            if not min_range <= value <= max_range:
                raise ValueError(f"Value for {self.variable_name} out of range: {min_range} to {max_range}")

            return Variable(value, self.var_is_constant.get(), min_range, max_range, self.variable_name)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input for {self.variable_name}: {e}")
            return None