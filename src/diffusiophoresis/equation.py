from diffusiophoresis.variable import Variable
from diffusiophoresis.diffusiophoresis_formulas import DiffusiophoresisFormulas as formula
from diffusiophoresis.variable_definitions import VariableDefinitions
class Equation():
    def __init__(self) -> None:
        self._variables: dict = VariableDefinitions.get_variables()



    ##Utility Methods
    def has_variable(self, name: str) -> bool:
        return name in self._variables
    
    def add_variable(self, variable: Variable):
        self._variables[variable.get_name()] = variable

    def randomize_equation(self) -> None:
        for variable in self._variables.values():
            variable.randomize()
        return self
    
    ##Accessor Methods
    def get_value(self, name: str) -> float:
        return self.get_variable(name).get_value()
    
    def get_variable(self, name: str) -> Variable:
        if name in self._variables:
            return self._variables[name]
        raise KeyError(f"Variable '{name}' not found in the equation")
    
    def get_index(self, index: int) -> Variable:
        if index < 0 or index >= len(self._variables):
            length: str = len(self._variables)
            raise IndexError("Index '{index}' out of range for dictionary of size '{length}'")
        
        variable_list : list = list(self._variables.values())
        return variable_list[index]
    
    def get_variable_list(self, filter_constants=False) -> list:
        if filter_constants == True:
            return [variable for variable in self._variables.values() if not variable.is_constant()]
        
        return list(self._variables.values())

    ##Mutator Methods
    def set_value(self, name: str, value: float, safe_mode=False) -> None:
        #raises error if variable is constant
        variable = self.get_variable(name)
        variable.set_value(value, safe_mode)
    
    def set_variable(self, variable: Variable):
        self._variables[variable.get_name()] = variable

    def set_variable_list(self, variable_list: list) -> list:
        for variable in variable_list:
            self.set_variable(variable)

    ##Calculations
    def optimize(self) -> float:
        #defines what this equation aims to optimize
        return self.get_exclusion_zone_area() #TODO *clean flow rate (not implemented)
    
    def get_exclusion_zone_area(self) -> float:
        if self.has_variable("exclusion_zone_area"):
            return self.get_value("exclusion_zone_area")
        
        channel_height: float = self.get_value("channel_height")
        channel_length: float = self.get_value("channel_length")
        channel_width: float = self.get_value("channel_width")

        mean_velocity: float = 1 #need to get this value
        diffusiophoretic_velocity: float = self.get_diffusiophoretic_velocity()
        return formula.exclusion_zone_area(channel_height, channel_length, channel_width, mean_velocity, diffusiophoretic_velocity)
    
    def get_diffusiophoretic_velocity(self) -> float:
        if self.has_variable("diffusiophoretic_velocity"):
            return self.get_value("diffusiophoretic_velocity")
        
        diffusiophoretic_mobility : float = self.get_diffusiophoretic_mobility()
        chemiphoretic_gradient: float = self.get_chemiphoretic_gradient()
        return formula.diffusiophoretic_velocity(diffusiophoretic_mobility, chemiphoretic_gradient)

    def get_beta_potential(self) -> float:
        if self.has_variable("beta_potential"):
            return self.get_value("beta_potential")
        
        else:
            cation: float = self.get_value("cation")
            anion: float = self.get_value("anion")
            return formula.beta_potential(cation, anion)

    def get_diffusiophoretic_mobility(self) -> float:
        if self.has_variable("diffusiophoretic_mobility"):
            return self.get_value("diffusiophoretic_mobility")
        
        beta_potential: float = self.get_beta_potential()
        electrophoretic_mobility: float = self.get_electrophoretic_mobility()
        chemiphoretic_mobility: float = self.get_chemiphoretic_mobility()
        return formula.diffusiophoretic_mobility(electrophoretic_mobility, chemiphoretic_mobility, beta_potential)
    
    def get_electrophoretic_mobility(self) -> float:
        if self.has_variable("electrophoretic_mobility"):
            return self.get_value("electrophoretic_mobility")
        
        valence_charge: float = self.get_value("valence_charge")
        elementary_charge: float = self.get_value("elementary_charge")
        zeta_potential: float = self.get_value("zeta_potential")
        absolute_temperature: float = self.get_value("absolute_temperature")
        return formula.electrophoretic_mobility(valence_charge, elementary_charge, zeta_potential, absolute_temperature)
        
    def get_chemiphoretic_mobility(self) -> float:
        if self.has_variable("chemiphoretic_mobility"):
            return self.get_value("chemiphoretic_mobility")
        
        valence_charge: float = self.get_value("valence_charge")
        elementary_charge: float = self.get_value("elementary_charge")
        zeta_potential: float = self.get_value("zeta_potential")
        absolute_temperature: float = self.get_value("absolute_temperature")
        return formula.chemiphoretic_mobility(valence_charge, elementary_charge, zeta_potential, absolute_temperature)
    
    def get_chemiphoretic_gradient(self) -> float:
        if self.has_variable("chemiphoretic_gradient"):
            return self.get_value("chemiphoretic_gradient")
        
        c_initial: float = self.get_value("c_initial") #background concentration
        channel_height: float = self.get_value("channel_height")
        return formula.chemiphoretic_gradient(c_initial, channel_height)

    def get_channel_area(self) -> float:
        if self.has_variable("channel_area"):
            return self.get_value("channel_area")
        
        channel_height: float = self.get_value("channel_height")
        channel_width: float = self.get_value("channel_width")
        return formula.channel_area(channel_height, channel_width)
    
    def get_characteristic_length(self) -> float:
        if self.has_variable("characteristic_length"):
            return self.get_value("characteristic_length")
        
        channel_height: float = self.get_value("channel_height")
        channel_width: float = self.get_value("channel_width")

        return formula.characteristic_length(channel_height, channel_width)

    def is_laminar(self) -> bool:
        fluid_density: float = self.get_value("fluid_density")
        fluid_velocity: float = self.get_value("fluid_velocity")
        characteristic_length: float = self.get_characteristic_length()
        dynamic_viscosity: float = self.get_value("dynamic_viscosity")
        
        reynolds_number: float = formula.reynolds_number(fluid_density, fluid_velocity, characteristic_length, dynamic_viscosity)
        return reynolds_number < 500

    ##Magic Methods
    def __str__(self) -> str:
        variables: str = ', '.join(str(variable) for variable in self._variables.values())
        return f"{variables}"

    def __hash__(self) -> int:
        sorted_vars: list[tuple[str, Variable]] = sorted(self._variables.items())#sort variables by name for consistent hashing
        return hash(tuple((name, hash(var)) for name, var in sorted_vars))

    def __eq__(self, other) -> bool:
        if isinstance(other, Equation):
            return self._variables == other._variables
        return False