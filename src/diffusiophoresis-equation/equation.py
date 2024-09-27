from equation_formulas import Equation_Formulas
from ..simulations.diffusiophoretic_particle_tracker import DiffusiophoreticParticleTracker
from variable import Variable
import numpy as np
class Equation(Equation_Formulas):
    def __init__(self, absolute_temperature, electrophoretic_mobility, chemiphoretic_mobility) -> None:
        super().__init__()
        self.variable_array = np.array()
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

        self.particle_tracker : DiffusiophoreticParticleTracker = DiffusiophoreticParticleTracker()
        #set constant flags:
        self.constant_flags = {
            'absolute_temperature': False
        }
    
    def get_variable(self, name):
        return

    def set_variable(self, name, value):
        pass
    
    def get_variable_names_list(self) -> list:
        return 
    
    def get_variable_array(self) -> np.array:
        return
    
    def get_channel_area(self) -> float:
        return self.channel_height * self.channel_width
    
    def set_calculated_electrophoretic_mobility(self, valence_charge, elementary_charge, zeta_potential, cation, anion):
        return 2 * self.beta_potential(cation, anion) * self.electrophoretic_mobility(valence_charge, elementary_charge, zeta_potential)
    
    def set_calculated_chemiphoretic_mobility(self, valence_charge, elementary_charge, zeta_potential):
        return self.chemiphoretic_mobility(valence_charge, elementary_charge, zeta_potential)
    
    def is_laminar(self) -> bool:
        self.reynolds_number(self.density, self.fluid_velocity, self.characteristic_length, self.dynamic_viscosity)
    
    def get_exclusion_zone_area(self) -> float:
        return self.particle_tracker.calculate_exclusion_zone_area()#need to pass parameters