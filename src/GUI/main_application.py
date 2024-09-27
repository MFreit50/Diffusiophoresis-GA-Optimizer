import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from variable_entry import VariableEntry

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Variable Input GUI")

        # Configure grid for centering
        self.grid_columnconfigure(0, weight=1)  # Center the labels column
        self.grid_columnconfigure(1, weight=1)  # Center the entry fields column
        
        # Variables
        self.variables = {}

        # Absolute Temperature
        self.temp_label = ttk.Label(self, text="Absolute Temperature")
        self.temp_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.temp_entry = VariableEntry(self, "", 0.0, 1000.0)
        self.temp_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # Fluid Density
        self.density_label = ttk.Label(self, text="Fluid Density")
        self.density_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.density_entry = VariableEntry(self, "", 0.0, 2000.0)
        self.density_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Fluid Viscosity
        self.viscosity_label = ttk.Label(self, text="Fluid Viscosity")
        self.viscosity_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.viscosity_entry = VariableEntry(self, "", 0.0, 10.0)
        self.viscosity_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        # Channel Length
        self.length_label = ttk.Label(self, text="Channel Length")
        self.length_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.length_entry = VariableEntry(self, "", 0.0, 10.0)
        self.length_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Channel Height
        self.height_label = ttk.Label(self, text="Channel Height")
        self.height_label.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.height_entry = VariableEntry(self, "", 0.0, 1000.0)
        self.height_entry.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        # Fluid Velocity
        self.velocity_label = ttk.Label(self, text="Fluid Velocity")
        self.velocity_label.grid(row=5, column=0, padx=10, pady=10, sticky='e')
        self.velocity_entry = VariableEntry(self, "", 0.0, 1000.0)
        self.velocity_entry.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        # Beta Potential
        self.beta_potential_label = ttk.Label(self, text="Beta Potential")
        self.beta_potential_label.grid(row=6, column=0, padx=10, pady=10, sticky='e')
        self.beta_potential_entry = VariableEntry(self, "", -1000.0, 1000.0)
        self.beta_potential_entry.grid(row=6, column=1, padx=10, pady=10, sticky='w')

        self.beta_checkbox = ttk.Checkbutton(self, text="Use Cation/Anion instead", command=self.toggle_cation_anion)
        self.beta_checkbox.grid(row=6, column=2, padx=10, pady=10, sticky='w')

        self.cation_label = ttk.Label(self, text="Cation")
        self.anion_label = ttk.Label(self, text="Anion")
        self.cation_entry = VariableEntry(self, "", 0.0, 1000.0)
        self.anion_entry = VariableEntry(self, "", 0.0, 1000.0)
        self.cation_label.grid_remove()
        self.anion_label.grid_remove()
        self.cation_entry.grid_remove()
        self.anion_entry.grid_remove()

        # Chemiphoretic Gradient
        self.chemiphoretic_gradient_label = ttk.Label(self, text="Chemiphoretic Gradient")
        self.chemiphoretic_gradient_label.grid(row=7, column=0, padx=10, pady=10, sticky='e')
        self.chemiphoretic_gradient_entry = VariableEntry(self, "", 0.0, 1000.0)
        self.chemiphoretic_gradient_entry.grid(row=7, column=1, padx=10, pady=10, sticky='w')

        self.chem_checkbox = ttk.Checkbutton(self, text="Use Ci/Cb instead", command=self.toggle_ci_cb)
        self.chem_checkbox.grid(row=7, column=2, padx=10, pady=10, sticky='w')

        self.ci_label = ttk.Label(self, text="Ci")
        self.cb_label = ttk.Label(self, text="Cb")
        self.ci_entry = VariableEntry(self, "", 0.0, 1000.0)
        self.cb_entry = VariableEntry(self, "", 0.0, 1000.0)
        self.ci_label.grid_remove()
        self.cb_label.grid_remove()
        self.ci_entry.grid_remove()
        self.cb_entry.grid_remove()

        # Electrophoretic Mobility
        self.electrophoretic_mobility_label = ttk.Label(self, text="Electrophoretic Mobility")
        self.electrophoretic_mobility_label.grid(row=8, column=0, padx=10, pady=10, sticky='e')
        self.electrophoretic_mobility_entry = VariableEntry(self, "", 0.0, 1000.0)
        self.electrophoretic_mobility_entry.grid(row=8, column=1, padx=10, pady=10, sticky='w')

        # Chemiphoretic Mobility
        self.chemiphoretic_mobility_label = ttk.Label(self, text="Chemiphoretic Mobility")
        self.chemiphoretic_mobility_label.grid(row=9, column=0, padx=10, pady=10, sticky='e')
        self.chemiphoretic_mobility_entry = VariableEntry(self, "", 0.0, 1000.0)
        self.chemiphoretic_mobility_entry.grid(row=9, column=1, padx=10, pady=10, sticky='w')

        # Button to submit the data
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=10, column=0, columnspan=2, padx=20, pady=20, sticky='nsew')

        # Configure row and column weights to make the layout dynamic
        for i in range(11):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def toggle_cation_anion(self):
        if self.beta_checkbox.instate(['selected']):
            self.cation_entry.grid()
            self.anion_entry.grid()
            self.beta_potential_entry.grid_remove()
        else:
            self.cation_entry.grid_remove()
            self.anion_entry.grid_remove()
            self.beta_potential_entry.grid()

    def toggle_ci_cb(self):
        if self.chem_checkbox.instate(['selected']):
            self.ci_entry.grid()
            self.cb_entry.grid()
            self.chemiphoretic_gradient_entry.grid_remove()
        else:
            self.ci_entry.grid_remove()
            self.cb_entry.grid_remove()
            self.chemiphoretic_gradient_entry.grid()

    def submit(self):
        # Collect data from each variable entry
        self.variables['Absolute Temperature'] = self.temp_entry.get_value()
        self.variables['Fluid Density'] = self.density_entry.get_value()
        self.variables['Fluid Viscosity'] = self.viscosity_entry.get_value()
        self.variables['Channel Length'] = self.length_entry.get_value()
        self.variables['Channel Height'] = self.height_entry.get_value()
        self.variables['Fluid Velocity'] = self.velocity_entry.get_value()
        if self.beta_checkbox.instate(['selected']):
            self.variables['Cation'] = self.cation_entry.get_value()
            self.variables['Anion'] = self.anion_entry.get_value()
        else:
            self.variables['Beta Potential'] = self.beta_potential_entry.get_value()
        if self.chem_checkbox.instate(['selected']):
            self.variables['Ci'] = self.ci_entry.get_value()
            self.variables['Cb'] = self.cb_entry.get_value()
        else:
            self.variables['Chemiphoretic Gradient'] = self.chemiphoretic_gradient_entry.get_value()
        self.variables['Electrophoretic Mobility'] = self.electrophoretic_mobility_entry.get_value()
        self.variables['Chemiphoretic Mobility'] = self.chemiphoretic_mobility_entry.get_value()

        # Check for any None values (invalid inputs)
        if any(var is None for var in self.variables.values()):
            return  # Invalid input, stop further processing
        
        # Process variables or pass to the next step in the system
        messagebox.showinfo("Success", "All variables have been collected successfully!")
