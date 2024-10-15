import tkinter as tk
from tkinter import ttk, simpledialog
from sympy import sympify, latex
from sympy.core.sympify import SympifyError
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SymbolPanel:
    def __init__(self, parent, input_var):
        self.frame = tk.Frame(parent)
        self.input_var = input_var
        self.is_expanded = False

        self.toggle_button = tk.Button(parent, text="Show Symbols", command=self.toggle_panel)
        self.toggle_button.pack()

        self.add_symbol_button(r"\int", "∫")
        self.add_symbol_button(r"\frac{}{}", "a/b")
        self.add_symbol_button(r"\sqrt{}", "√")
        self.add_symbol_button(r"\pi", "π")
        self.add_symbol_button(r"\sin", "sin()")
        self.add_symbol_button(r"\cos", "cos()")
        self.add_symbol_button(r"\tan", "tan()")

    def add_symbol_button(self, symbol, display_text):
        button = tk.Button(self.frame, text=display_text, command=lambda: self.insert_symbol(symbol))
        button.pack(side=tk.LEFT, padx=5)

    def insert_symbol(self, symbol):
        current_text = self.input_var.get()
        self.input_var.set(current_text + symbol)

    def toggle_panel(self):
        if self.is_expanded:
            self.frame.pack_forget()
            self.toggle_button.config(text="Show Symbols")
        else:
            self.frame.pack(pady=5)
            self.toggle_button.config(text="Hide Symbols")
        self.is_expanded = not self.is_expanded


class EquationFormatterApp:
    def __init__(self, root, formulas_table):
        self.root = root
        self.formulas_table = formulas_table
        self.root.title("Equation Formatter")

        self.input_var = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.input_var, width=50)
        self.entry.pack(pady=10)

        self.fig, self.ax = plt.subplots(figsize=(5, 2), dpi=100)
        self.ax.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        self.input_var.trace_add("write", self.update_equation)
        self.symbol_panel = SymbolPanel(root, self.input_var)

        self.submit_button = tk.Button(root, text="Submit Formula", command=self.submit_formula)
        self.submit_button.pack(pady=10)

    def update_equation(self, *args):
        user_input = self.input_var.get()
        try:
            expr = sympify(user_input)
            latex_expr = latex(expr)
        except SympifyError:
            latex_expr = user_input
        
        self.ax.clear()
        self.ax.axis('off')
        self.ax.text(0.5, 0.5, f"${latex_expr}$", horizontalalignment='center', verticalalignment='center', fontsize=18)
        self.canvas.draw()

    def submit_formula(self):
        formula_name = simpledialog.askstring("Formula Name", "Enter a name for this formula:")
        if formula_name:
            formula_expression = self.input_var.get()
            self.formulas_table.insert_formula(formula_name, formula_expression)


class FormulaTable:
    def __init__(self, parent):
        self.parent = parent
        self.formulas = []
        
        self.table = ttk.Treeview(parent, columns=("Name", "Expression"), show="headings")
        self.table.heading("Name", text="Formula Name")
        self.table.heading("Expression", text="Expression")
        self.table.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.delete_button = tk.Button(parent, text="Delete Selected Formula", command=self.delete_formula)
        self.delete_button.pack(side=tk.BOTTOM)

    def insert_formula(self, name, expression):
        self.formulas.append((name, expression))
        self.table.insert("", "end", values=(name, expression))

    def delete_formula(self):
        selected_item = self.table.selection()
        if selected_item:
            for item in selected_item:
                self.table.delete(item)


class VariableTable:
    def __init__(self, parent):
        self.variables = []
        
        # Create a frame to contain both the table and the buttons
        self.frame = tk.Frame(parent)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create the table for variables
        self.table = ttk.Treeview(self.frame, columns=("Name", "Symbol"), show="headings")
        self.table.heading("Name", text="Variable Name")
        self.table.heading("Symbol", text="Symbol")
        self.table.pack(fill=tk.BOTH, expand=True)

        # Create a button frame for the buttons
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(fill=tk.X)

        # Buttons for adding and deleting variables, packed at the bottom
        self.add_button = tk.Button(self.button_frame, text="Add Variable", command=self.add_variable)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Selected Variable", command=self.delete_variable)
        self.delete_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def add_variable(self):
        name = simpledialog.askstring("Variable Name", "Enter variable name:")
        symbol = simpledialog.askstring("Variable Symbol", "Enter variable symbol:")
        if name and symbol:
            self.insert_variable(name, symbol)

    def insert_variable(self, name, symbol):
        self.variables.append((name, symbol))
        self.table.insert("", "end", values=(name, symbol))

    def delete_variable(self):
        selected_item = self.table.selection()
        if selected_item:
            for item in selected_item:
                self.table.delete(item)


class EquationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Equation Builder")

        # Create a frame for variable and formula tables
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create the Variable and Formula tables
        self.variable_table = VariableTable(self.frame)
        self.formula_table = FormulaTable(self.frame)

        # Create the equation formatter app
        self.formatter_app = EquationFormatterApp(root, self.formula_table)

        # Add some dummy variables for testing
        self.variable_table.insert_variable("x", "x")
        self.variable_table.insert_variable("y", "y")


if __name__ == "__main__":
    root = tk.Tk()
    app = EquationApp(root)
    root.mainloop()