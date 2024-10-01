import json
from diffusiophoresis.variable import Variable

class DataEngine:
    @staticmethod
    def read_variable_list() -> list:
        """
        Reads a list of Variable objects from a JSON file and converts them back into Variable instances.

        Returns
        -------
        list
            A list of Variable objects read from the file.
        """
        with open("variable_list.json", 'r') as file:
            variable_data = json.load(file)
        
        return [Variable.from_dict(item) for item in variable_data]

    @staticmethod
    def write_variable_list(variable_list: list) -> None:
        """
        Writes a list of Variable objects to a JSON file by converting them into dictionary form.

        Parameters
        ----------
        variable_list : list
            A list of Variable objects to write to the file.
        """
        with open("variable_list.json", 'w') as file:
            json.dump([var.to_dict() for var in variable_list], file, indent=4)