import tkinter as tk
import threading
from diffusiophoresis.equation import Equation
from ga.genetic_algorithm import GeneticAlgorithm
from diffusiophoresis.variable_definitions import VariableDefinitions
from diffusiophoresis.variable import Variable
from Modules.data_broadcaster import DataBroadcaster
from GUI.ga_gui import GA_GUI
from ga.genetic_algorithm_builder import GeneticAlgorithmBuilder

class MainCoordinator:
    def __init__(self) -> None:
        #self.data_engine = DataEngine()
        pass

    def initialize(self):
        VariableDefinitions.load_rastrigin()

        root = tk.Tk()
        gui = GA_GUI(root)


        # Create and run the GA
        ga_builder = GeneticAlgorithmBuilder(generations=10000, population_size=1000)
        ga = ga_builder.build()
        ga.subscribe(gui)
        
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