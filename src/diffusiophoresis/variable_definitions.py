import copy
class VariableDefinitions():
    variables = {}

    @staticmethod
    def get_variables():
        return copy.deepcopy(VariableDefinitions.variables)