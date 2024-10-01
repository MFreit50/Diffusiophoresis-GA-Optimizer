from diffusiophoresis.variable import Variable
from diffusiophoresis.diffusiophoresis_formulas import DiffusiophoresisFormulas as formula

class Equation():
    def __init__(self) -> None:
        super().__init__()
        self.variables = {}

    def has_variable(self, name : str) -> bool:
        return name in self.variables
    
    def add_variable(self, variable : Variable):
        self.variables[variable.get_name()] = variable

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        raise KeyError(f"Variable '{name}' not found in the equation")
    
    def get_value(self, name):
        return self.get_variable(name).value
    
    def set_value(self, name, value):
        #raises error if variable is constant
        variable = self.get_variable(name)
        variable.set_value(value)
    
    def get_variable_names_list(self) -> list:
        return list(self.variables)

    def randomize_equation(self) -> None:
        for _, variable in self.variables.items():
            variable.randomize()

    def channel_area(self) -> float:
        channel_height = self.get_value("channel_height")
        channel_length = self.get_value("channel_length")
        return channel_height * channel_length
    
    #Calculations
    def get_exlcusion_zone_area(self):
        channel_height = self.get_value("channel_height")
        channel_length = self.get_value("channel_height")
        mean_velocity = 1 #need to get this value
        diffusiophoretic_velocity = self.get_diffusiophoretic_velocity()
        return formula.exclusion_zone_area(channel_height, channel_length, mean_velocity, diffusiophoretic_velocity)
    
    def get_diffusiophoretic_velocity(self) -> float:
        beta_potential = self.get_beta_potential()
        electrophoretic_mobility = self.get_electrophoretic_mobility()
        chemiphoretic_mobility = self.get_chemiphoretic_mobility()
        chemiphoretic_gradient = self.get_chemiphoretic_gradient()
        return formula.diffusiophoretic_velocity(beta_potential, electrophoretic_mobility, chemiphoretic_mobility, chemiphoretic_gradient)

    def get_beta_potential(self):
        if self.has_variable("beta_potential"):
            return self.get_value("beta_potential")
        else:
            cation = self.get_value("cation")
            anion = self.get_value("anion")
            return formula.beta_potential(cation, anion)

    def get_electrophoretic_mobility(self) -> float:
        valence_charge = self.get_value("valence_charge")
        elementary_charge = self.get_value("elementary_charge")
        zeta_potential = self.get_value("zeta_potential")
        absolute_temperature = self.get_value("absolute_temperature")
        return formula.electrophoretic_mobility(valence_charge, elementary_charge, zeta_potential, absolute_temperature)
        
    def get_chemiphoretic_mobility(self) -> float:
        valence_charge = self.get_value("valence_charge")
        elementary_charge = self.get_value("elementary_charge")
        zeta_potential = self.get_value("zeta_potential")
        absolute_temperature = self.get_value("absolute_temperature")
        return formula.chemiphoretic_mobility(valence_charge, elementary_charge, zeta_potential, absolute_temperature)
    
    def get_chemiphoretic_gradient(self) -> float:
        ci = self.get_value("ci")
        cb = self.get_value("cb")
        channel_length = self.get_value("length")
        return formula.chemiphoretic_gradient(ci, cb, channel_length)

    def is_laminar(self) -> bool:
        fluid_density = self.get_value("fluid_density")
        fluid_velocity = self.get_value("fluid_velocity")
        characteristic_length = self.get_characteristic_length()
        dynamic_viscosity = self.get_value("dynamic_viscosity")
        reynolds_number = formula.reynolds_number(fluid_density, fluid_velocity, characteristic_length, dynamic_viscosity)
        return reynolds_number < 500