import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from variable_entry import VariableEntry

class MainApplication(tk.Tk):
    def __init__(self, variable_list, coordinator):
        super().__init__()
        self.title("Variable Input GUI")

        # Coordinator reference
        self.coordinator = coordinator

        # Configure grid for layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Variables
        self.variables = {}

        # Create labels and entries based on variable_list
        for i, variable in enumerate(variable_list):
            label_text = variable.variable_name
            min_value = variable.min_range
            max_value = variable.max_range

            label = ttk.Label(self, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky='e')

            entry = VariableEntry(self, "", min_value, max_value)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky='w')
            self.variables[label_text] = entry

        # Submit button to collect and process data
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=len(variable_list), column=0, columnspan=2, padx=20, pady=20, sticky='nsew')

        # Configure dynamic layout
        for i in range(len(variable_list) + 1):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def submit(self):
        # Collect data from the GUI into a list
        collected_variables = []

        for label, entry in self.variables.items():
            value = entry.get_value()
            if value is None:
                return  # Invalid input, already handled by the error message
            collected_variables.append(value)  # Collect Variable objects into the list

        # Pass the collected data as a list of Variable objects to the coordinator
        self.coordinator.update_variable_list(collected_variables)
        messagebox.showinfo("Success", "All variables have been collected and processed.")