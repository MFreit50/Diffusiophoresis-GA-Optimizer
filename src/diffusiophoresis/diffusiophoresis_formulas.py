import math
import numpy as np
from scipy.integrate import trapezoid

class DiffusiophoresisFormulas:
    """
    A class containing various static methods to perform calculations related to 
    diffusiophoresis, fluid dynamics, and particle trajectories in channels.
    """

    @staticmethod
    def exclusion_zone_area(channel_height, channel_length, channel_width, mean_flow_velocity, diffusiophoretic_velocity) -> float:
        """
        Calculates the exclusion zone area by integrating the particle trajectory 
        within a channel based on flow and diffusiophoretic velocity.

        Parameters:
            channel_height (float): The height of the channel (in micrometers).
            channel_length (float): The length of the channel (in centimeters).
            channel_width (float): The width of the channel (in centimeters).
            mean_flow_velocity (float): The average flow velocity through the channel (in mm/s).
            diffusiophoretic_velocity (float): The diffusiophoretic velocity of particles (in µm/s).

        Returns:
            float: The total exclusion zone area (in µm²).
        """
        h, l, w, v, u = DiffusiophoresisFormulas._convert_variables(channel_height, channel_length, channel_width, mean_flow_velocity, diffusiophoretic_velocity)
        exclusion_zone_area, exclusion_zone_velocity = DiffusiophoresisFormulas._calculate_exclusion_zone_area_and_velocity(h, l, w, v, u)
        return exclusion_zone_area * exclusion_zone_velocity

    @staticmethod
    def diffusiophoretic_velocity(diffusiophoretic_mobility, chemiphoretic_gradient) -> float:
        """
        Calculate the diffusiophoretic velocity of particles based on diffusiophoretic mobility 
        and the chemiphoretic gradient.

        Parameters:
            diffusiophoretic_mobility (float): The diffusiophoretic mobility of the particles.
            chemiphoretic_gradient (float): The gradient of chemical concentrations.

        Returns:
            float: Calculated diffusiophoretic velocity (in m/s).
        """
        return diffusiophoretic_mobility * chemiphoretic_gradient

    @staticmethod
    def diffusiophoretic_mobility(electrophoretic_mobility, chemiphoretic_mobility, beta_potential) -> float:
        """
        Calculate the total diffusiophoretic mobility of particles based on electrophoretic 
        and chemiphoretic mobilities and the beta potential.

        Parameters:
            electrophoretic_mobility (float): The electrophoretic mobility of the particles.
            chemiphoretic_mobility (float): The chemiphoretic mobility of the particles.
            beta_potential (float): The beta potential difference between cation and anion concentrations.

        Returns:
            float: The calculated diffusiophoretic mobility.
        """
        return 2 * beta_potential * electrophoretic_mobility + chemiphoretic_mobility

    @staticmethod
    def electrophoretic_mobility(valence_charge, elementary_charge, zeta_potential, absolute_temperature) -> float:
        """
        Calculate the electrophoretic mobility of particles in a fluid.

        Parameters:
            valence_charge (float): The valence of the ion (dimensionless).
            elementary_charge (float): The elementary charge (in Coulombs).
            zeta_potential (float): The zeta potential of the particles (in Volts).
            absolute_temperature (float): The temperature of the fluid (in Kelvin).

        Returns:
            float: The calculated electrophoretic mobility (in m²/V·s).
        """
        boltzmann_constant = 1.380649e-23  # J/K
        return (valence_charge * elementary_charge * zeta_potential) / (boltzmann_constant * absolute_temperature)

    @staticmethod
    def chemiphoretic_mobility(valence_charge, elementary_charge, zeta_potential, absolute_temperature) -> float:
        """
        Calculate the chemiphoretic mobility of particles based on their potential and temperature.

        Parameters:
            valence_charge (float): The valence of the ion (dimensionless).
            elementary_charge (float): The elementary charge (in Coulombs).
            zeta_potential (float): The zeta potential of the particles (in Volts).
            absolute_temperature (float): The temperature of the fluid (in Kelvin).

        Returns:
            float: The calculated chemiphoretic mobility.
        """
        boltzmann_constant = 1.380649e-23  # J/K
        return 8 * math.log(math.cosh(
            (valence_charge * elementary_charge * zeta_potential) / 
            (4 * absolute_temperature * boltzmann_constant)
        ))

    @staticmethod
    def chemiphoretic_gradient(c_initial, channel_height) -> float:
        """
        Calculate the chemiphoretic gradient based on initial concentration and channel height.

        Parameters:
            c_initial (float): Initial concentration.
            channel_height (float): Height of the channel (in meters).

        Returns:
            float: The calculated chemiphoretic gradient.
        """
        return abs(math.log(5 / c_initial) / channel_height)

    @staticmethod
    def beta_potential(cation, anion) -> float:
        """
        Calculate the beta potential based on the concentrations of cations and anions.

        Parameters:
            cation (float): Concentration of cations.
            anion (float): Concentration of anions.

        Returns:
            float: The calculated beta potential.
        """
        return (cation - anion) / (cation + anion)

    @staticmethod
    def reynolds_number(density, velocity, characteristic_length, dynamic_viscosity) -> float:
        """
        Calculate the Reynolds number, a dimensionless quantity that describes the flow of the fluid.

        Parameters:
            density (float): The density of the fluid (in kg/m³).
            velocity (float): The velocity of the fluid (in m/s).
            characteristic_length (float): A characteristic length of the flow (in meters).
            dynamic_viscosity (float): The dynamic viscosity of the fluid (in Pa·s).

        Returns:
            float: The calculated Reynolds number.
        """
        return (density * velocity * characteristic_length) / dynamic_viscosity

    @staticmethod
    def channel_area(height, width) -> float:
        """
        Calculate the area of the channel cross-section.

        Parameters:
            height (float): Height of the channel.
            width (float): Width of the channel.

        Returns:
            float: The area of the channel.
        """
        return height * width

    @staticmethod
    def characteristic_length(height, width) -> float:
        """
        Calculate the hydraulic diameter, which serves as the characteristic length 
        for a rectangular channel.

        Parameters:
            height (float): Height of the channel.
            width (float): Width of the channel.

        Returns:
            float: The hydraulic diameter (in meters).
        """
        area_rectangle = height * width
        perimeter_rectangle = 2 * (height + width)
        return (4 * area_rectangle) / perimeter_rectangle

    @staticmethod
    def flow_rate(area, average_velocity) -> float:
        """
        Calculate the flow rate of fluid through the channel.

        Parameters:
            area (float): Cross-sectional area of the channel.
            average_velocity (float): Average velocity of the fluid.

        Returns:
            float: The flow rate (in m³/s).
        """
        return area * average_velocity

    @staticmethod
    def pressure_drop(flow_rate, fluid_viscosity, channel_length, characteristic_length) -> float:
        """
        Calculate the pressure drop in the channel using the Hagen–Poiseuille equation.

        Parameters:
            flow_rate (float): Flow rate of the fluid.
            fluid_viscosity (float): Viscosity of the fluid (in Pa·s).
            channel_length (float): Length of the channel.
            characteristic_length (float): Hydraulic diameter of the channel.

        Returns:
            float: The pressure drop (in Pascals).
        """
        return flow_rate * (8 * fluid_viscosity * channel_length) / (math.pi * characteristic_length**4)

    # Private methods

    @staticmethod
    def _convert_variables(channel_height, channel_length, channel_width, mean_flow_velocity, diffusiophoretic_velocity) -> tuple:
        """
        Convert variables to SI units for calculations.

        Parameters:
            channel_height (float): Channel height in micrometers.
            channel_length (float): Channel length in centimeters.
            channel_width (float): Channel width in centimeters.
            mean_flow_velocity (float): Flow velocity in mm/s.
            diffusiophoretic_velocity (float): Diffusiophoretic velocity in µm/s.

        Returns:
            tuple: Converted values for channel height (m), channel length (m), 
                   channel width (m), mean flow velocity (m/s), and diffusiophoretic velocity (m/s).
        """
        channel_height *= 10**-6            # µm to meters
        channel_length *= 10**-2            # cm to meters
        channel_width *= 10**-2             # cm to meters
        mean_flow_velocity *= 10**-3        # mm/s to m/s
        diffusiophoretic_velocity *= 10**-6 # µm/s to m/s

        return channel_height, channel_length, channel_width, mean_flow_velocity, diffusiophoretic_velocity

    @staticmethod
    def _calculate_exclusion_zone_area_and_velocity(channel_height, channel_length, channel_width, mean_flow_velocity, diffusiophoretic_velocity) -> tuple:
        """
        Private method to calculate exclusion zone area and velocity.
        
        Parameters:
            channel_height (float): Channel height (m).
            channel_length (float): Channel length (m).
            channel_width (float): Channel width (m).
            mean_flow_velocity (float): Mean flow velocity (m/s).
            diffusiophoretic_velocity (float): Diffusiophoretic velocity (m/s).
        
        Returns:
            tuple: Calculated exclusion zone area (µm²) and velocity (m/s).
        """
        number_of_particles = 1
        number_of_points = 200
        y = np.linspace(start=0, stop=channel_height, num=number_of_particles)  # Particle Y positions
        time = np.linspace(start=0, stop=200, num=number_of_points)             # Time vector (0 to 200 seconds)

        # Calculate particle position
        x_pos, y_pos = DiffusiophoresisFormulas._calculate_particle_position(channel_height,  mean_flow_velocity, diffusiophoretic_velocity, time, y)
        exclusion_zone_height = y_pos[-1] #Last Y_pos
        #exclusion zone area
        exclusion_zone_area = exclusion_zone_height * channel_width
        exclusion_zone_velocity = 1/exclusion_zone_height * DiffusiophoresisFormulas._integrate(y_pos, 0, exclusion_zone_height)
        return exclusion_zone_area, exclusion_zone_velocity
    
    @staticmethod
    def _calculate_particle_position(h, v, u, t, y) -> tuple:
        """
        Calculates the X and Y positions of the particle over time.

        Args:
            h (float): Height of the channel in meters.
            v (float): Mean flow velocity in meters/second.
            u (float): Diffusiophoretic velocity in meters/second.
            t (array): Array of time steps.
            y (array): Array of initial Y positions of the particles.

        Returns:
            tuple: X and Y positions of the particles over time.
        """

        # Calculate the X and Y positions based on time and initial conditions
        x_pos = (10**6 * 6 * v) * (((u * t**2) / (2*h)) - ((u**2 * t**3) / (3 * h**2)) + ((y * t) / h) - ((u * y * t**2) / h**2) - ((y**2 * t) / h**2))
        y_pos = (u * t + y) * 10**6  # Convert Y position to micrometers
        return (x_pos, y_pos)

    @staticmethod
    def _integrate(y, a, b) -> float:
        """
        Computes the area under the particle trajectory by integrating the path length.

        Args:
            y (array): Y positions of the particle trajectory.

        Returns:
            float: The integrated area under the trajectory.
        """
        x = np.linspace(a, b, len(y))
        area = trapezoid(y, x)
        return area