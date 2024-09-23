from equation_formulas import Equation_Formulas
class Equation(Equation_Formulas):
    def __init__(self, absolute_temperature, electrophoretic_mobility, chemiphoretic_mobility) -> None:
        super().__init__()

        self.absolute_temperature = absolute_temperature

        #channel variables:
        self.channel_height
        self.channel_width

        #fluid variables:
        self.fluid_density
        self.fluid_viscosity
        self.fluid_velocity

        self.electrophoretic_mobility = electrophoretic_mobility
        self.chemiphoretic_mobility = chemiphoretic_mobility

        #set constant flags:
        self.constant_flags = {
            'absolute_temperature': False
        }
    
    
    def get_variable_names_list(self) -> list:
        return 
    
    def get_channel_area(self) -> float:
        return self.channel_height * self.channel_width
    
    def set_calculated_electrophoretic_mobility(self, valence_charge, elementary_charge, zeta_potential, cation, anion):
        return 2 * self.beta_potential(cation, anion) * self.electrophoretic_mobility(valence_charge, elementary_charge, zeta_potential)
    
    def set_calculated_chemiphoretic_mobility(self, valence_charge, elementary_charge, zeta_potential):
        return self.chemiphoretic_mobility(valence_charge, elementary_charge, zeta_potential)
    
    def is_laminar(self) -> bool:
        self.reynolds_number(self.density, self.fluid_velocity, self.characteristic_length, self.dynamic_viscosity)