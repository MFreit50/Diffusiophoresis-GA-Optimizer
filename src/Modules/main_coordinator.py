from Modules.data_engine import DataEngine
from main_application import MainApplication
from diffusiophoresis.variable_definitions import VariableDefinitions
class MainCoordinator:
    def __init__(self) -> None:
        self.data_engine = DataEngine()

    def initialize(self):
        # Read the variable list from the DataEngine
        variable_list = self.data_engine.read_variable_list()

        variables_dict = self.to_var_dict(variable_list)
        VariableDefinitions.variables = variables_dict

        # Pass both the variable list and self (coordinator) to MainApplication
        app = MainApplication(variable_list, coordinator=self)
        app.mainloop()

    def update_variable_list(self, collected_variables: list) -> None:
        self.data_engine.write_variable_list(collected_variables)
    
    def to_var_dict(variable_list : list) -> dict:
        #converts var list to dict as is used by the equation class
        var_dict = {}
        for var in variable_list:
            var_dict[var.get_name()] = var