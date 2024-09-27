import sys
import os

# Get the parent directory
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

        # Label
        ttk.Label(self, text=variable_name).grid(row=0, column=0)

        # Entry for variable value
        self.entry = ttk.Entry(self, textvariable=self.var_value)
        self.entry.grid(row=0, column=1)

        # Checkbox for constant
        self.constant_checkbox = ttk.Checkbutton(self, text="Constant", variable=self.var_is_constant)
        self.constant_checkbox.grid(row=0, column=2)

        # Set the range (optional)
        self.min_range = min_range
        self.max_range = max_range

    def get_value(self):
        try:
            value = self.var_value.get()
            if not self.min_range <= value <= self.max_range:
                raise ValueError(f"Value out of range for {self.variable_name}")
            return Variable(value, self.var_is_constant.get(), self.min_range, self.max_range, self.variable_name)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None