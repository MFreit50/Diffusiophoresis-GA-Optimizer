import os
import sys
import tkinter as tk
import threading
#from data_engine import DataEngine
#from main_application import MainApplication
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from diffusiophoresis.equation import Equation
from genetic_algorithm import GeneticAlgorithm
from diffusiophoresis.variable_definitions import VariableDefinitions
from diffusiophoresis.variable import Variable
from data_broadcaster import DataBroadcaster
from ga_gui import GA_GUI

class MainCoordinator:
    def __init__(self) -> None:
        #self.data_engine = DataEngine()
        pass

    def initialize(self):
        print("test")
        VariableDefinitions.variables = {
            "beta_potential": Variable(variable_name="beta_potential", value=25.0, is_constant=False, min_range=10.0, max_range=50.0),
            "electrophoretic_mobility": Variable(variable_name="electrophoretic_mobility", value=0.001, is_constant=False, min_range=0.0001, max_range=0.01),
            "chemiphoretic_mobility": Variable(variable_name="chemiphoretic_mobility", value=0.001, is_constant=False, min_range=0.0001, max_range=0.01),
            "chemiphoretic_gradient": Variable(variable_name="chemiphoretic_gradient", value=0.01, is_constant=False, min_range=0.001, max_range=0.1),
        }

        root = tk.Tk()
        gui = GA_GUI(root)

        # Create the broadcaster
        broadcaster = DataBroadcaster()
        broadcaster.subscribe(gui)

        # Create and run the GA
        ga = GeneticAlgorithm(generations=10000, population_size=50, crossover_rate=0.7, mutation_rate=0.01, broadcaster=broadcaster)
        
        # Run the GA in a separate thread to avoid blocking the GUI
        ga_thread = threading.Thread(target=ga.run)
        ga_thread.start()

        # Start the Tkinter main loop
        root.mainloop()
        
        #genetic_algorithm = GeneticAlgorithm(1000, 1000, 0.5, 0.6)
        #genetic_algorithm.run()
        # Read the variable list from the DataEngine
        #variable_list = self.data_engine.read_variable_list()

        #variables_dict = self.to_var_dict(variable_list)
        #VariableDefinitions.variables = variables_dict

        # Pass both the variable list and self (coordinator) to MainApplication
        #app = MainApplication(variable_list, coordinator=self)
        #app.mainloop()


    def update_variable_list(self, collected_variables: list) -> None:
        self.data_engine.write_variable_list(collected_variables)
    
    def to_var_dict(variable_list : list) -> dict:
        #converts var list to dict as is used by the equation class
        var_dict = {}
        for var in variable_list:
            var_dict[var.get_name()] = var