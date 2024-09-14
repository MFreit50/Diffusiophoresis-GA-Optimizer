import math
import numpy as np

class Equations:
    def __init__(self) -> None:
        """
        Initializes the Equations class and defines constants.
        """
        self.boltzmann_constant = 1.380649e-23  # in Joules per Kelvin (J/K)

    def diffusiophoretic_velocity(self, valence_charge, elementary_charge, zeta_potential, absolute_temperature, cation, anion, ci, cb, channel_length) -> float:
        """
        Calculate the diffusiophoretic velocity.

        Parameters:
            valence_charge: Charge of the ion (in Coulombs).
            elementary_charge: Elementary charge (in Coulombs).
            zeta_potential: Zeta potential (in Volts).
            absolute_temperature: Absolute temperature (in Kelvin).
            cation: Cation concentration.
            anion: Anion concentration.
            ci: Concentration at one end of the channel.
            cb: Concentration at the other end of the channel.
            channel_length: Length of the channel (in meters).
        
        Returns:
            float: Calculated diffusiophoretic velocity (in m/s).
        """
        electrophoretic_mobility = 2 * self.beta_potential(cation, anion) * \
            self.electrophoretic_mobility(valence_charge, elementary_charge, zeta_potential, absolute_temperature)
        chemiphoretic_mobility = self.chemiphoretic_mobility(valence_charge, elementary_charge, zeta_potential, absolute_temperature)
        chemiphoretic_gradient = self.chemiphoretic_gradient(ci, cb, channel_length)
        diffusiophoretic_velocity = chemiphoretic_gradient * (electrophoretic_mobility + chemiphoretic_mobility)
        return diffusiophoretic_velocity

    def reynolds_number(self, density, velocity, characteristic_length, dynamic_viscosity) -> float:
        """
        Calculate the Reynolds number.

        Parameters:
            density: Density of the fluid (in kg/m^3).
            velocity: Velocity of the fluid (in m/s).
            characteristic_length: Characteristic length (in meters).
            dynamic_viscosity: Dynamic viscosity of the fluid (in Pa·s).
        
        Returns:
            float: Calculated Reynolds number.
        """
        reynolds_number = (density * velocity * characteristic_length) / dynamic_viscosity
        return reynolds_number
    
    def electrophoretic_mobility(self, valence_charge, elementary_charge, zeta_potential, absolute_temperature) -> float:
        """
        Calculate the electrophoretic mobility.

        Parameters:
            valence_charge: Charge of the ion (in Coulombs).
            elementary_charge: Elementary charge (in Coulombs).
            zeta_potential: Zeta potential (in Volts).
            absolute_temperature: Absolute temperature (in Kelvin).
        
        Returns:
            float: Calculated electrophoretic mobility (in m^2/V·s).
        """
        electrophoretic_mobility = (valence_charge * elementary_charge * zeta_potential) / \
                                   (self.boltzmann_constant * absolute_temperature)
        return electrophoretic_mobility
    
    def chemiphoretic_mobility(self, valence_charge, elementary_charge, zeta_potential, absolute_temperature) -> float:
        """
        Calculate the chemiphoretic mobility.

        Parameters:
            valence_charge: Charge of the ion (in Coulombs).
            elementary_charge: Elementary charge (in Coulombs).
            zeta_potential: Zeta potential (in Volts).
            absolute_temperature: Absolute temperature (in Kelvin).
        
        Returns:
            float: Calculated chemiphoretic mobility.
        """
        chemiphoretic_mobility = 8 * math.log(math.cosh(
            (valence_charge * elementary_charge * zeta_potential) / 
            (4 * absolute_temperature * self.boltzmann_constant)
        ))
        return chemiphoretic_mobility
    
    def beta_potential(self, cation, anion) -> float:
        """
        Calculate the beta potential.

        Parameters:
            cation: Cation concentration.
            anion: Anion concentration.
        
        Returns:
            float: Calculated beta potential.
        """
        beta_potential = (cation - anion) / (cation + anion)
        return beta_potential

    def chemiphoretic_gradient(self, ci, cb, channel_length) -> float:
        """
        Calculate the chemiphoretic gradient.

        Parameters:
            ci: Concentration at one end of the channel.
            cb: Concentration at the other end of the channel.
            channel_length: Length of the channel (in meters).
        
        Returns:
            float: Calculated chemiphoretic gradient.
        """
        # Note: log((ci - cb) / channel_length) may result in invalid values if ci <= cb.
        chemiphoretic_gradient = np.log((ci - cb) / channel_length)
        return chemiphoretic_gradient