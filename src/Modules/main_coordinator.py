from Modules.data_engine import DataEngine
from main_application import MainApplication

class MainCoordinator:
    def __init__(self) -> None:
        self.data_engine = DataEngine()

    def initialize(self):
        # Read the variable list from the DataEngine
        variable_list = self.data_engine.read_variable_list()

        # Pass both the variable list and self (coordinator) to MainApplication
        app = MainApplication(variable_list, coordinator=self)
        app.mainloop()

    def update_variable_list(self, collected_variables: list) -> None:
        self.data_engine.write_variable_list(collected_variables)