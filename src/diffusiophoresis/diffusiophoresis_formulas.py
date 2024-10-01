import math
import numpy as np

class DiffusiophoresisFormulas:
    """
    A class containing various static methods to perform calculations related to 
    diffusiophoresis, fluid dynamics, and particle trajectories in channels.
    """

    @staticmethod
    def exclusion_zone_area(channel_height, channel_length, mean_flow_velocity, diffusiophoretic_velocity) -> float:
        """
        Calculates the exclusion zone area by integrating the particle trajectory 
        within a channel based on flow and diffusiophoretic velocity.

        Parameters:
            channel_height (float): The height of the channel (in micrometers).
            channel_length (float): The length of the channel (in centimeters).
            mean_flow_velocity (float): The average flow velocity through the channel (in mm/s).
            diffusiophoretic_velocity (float): The diffusiophoretic velocity of particles (in µm/s).

        Returns:
            float: The total exclusion zone area (in µm²).
        """
        h, l, v, u = DiffusiophoresisFormulas._convert_variables(channel_height, channel_length, mean_flow_velocity, diffusiophoretic_velocity)
        x_percentage, y_percentage = DiffusiophoresisFormulas._calculate_particle_trajectory(h, l, v, u)
        exclusion_zone_area = DiffusiophoresisFormulas._integrate(x_percentage, y_percentage)
        return exclusion_zone_area

    @staticmethod
    def diffusiophoretic_velocity(beta_potential, electrophoretic_mobility, chemiphoretic_mobility, chemiphoretic_gradient) -> float:
        """
        Calculate the diffusiophoretic velocity of particles based on electrophoretic and chemiphoretic properties.

        Parameters:
            beta_potential (float): The beta potential difference between the cation and anion concentrations.
            electrophoretic_mobility (float): The electrophoretic mobility of the particles.
            chemiphoretic_mobility (float): The chemiphoretic mobility of the particles.
            chemiphoretic_gradient (float): The gradient of chemical concentrations.

        Returns:
            float: Calculated diffusiophoretic velocity (in m/s).
        """
        diffusiophoretic_velocity = ((2 * beta_potential * electrophoretic_mobility) + chemiphoretic_mobility) * chemiphoretic_gradient
        return diffusiophoretic_velocity

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
        boltzmann_constant = 1.380649e-23  # in J/K
        electrophoretic_mobility = (valence_charge * elementary_charge * zeta_potential) / \
                                   (boltzmann_constant * absolute_temperature)
        return electrophoretic_mobility

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
        boltzmann_constant = 1.380649e-23  # in J/K
        chemiphoretic_mobility = 8 * math.log(math.cosh(
            (valence_charge * elementary_charge * zeta_potential) / 
            (4 * absolute_temperature * boltzmann_constant)
        ))
        return chemiphoretic_mobility

    @staticmethod
    def chemiphoretic_gradient(ci, cb, channel_length) -> float:
        """
        Calculate the chemiphoretic gradient based on concentration differences and channel length.

        Parameters:
            ci (float): Concentration at one end of the channel.
            cb (float): Concentration at the other end of the channel.
            channel_length (float): Length of the channel (in meters).

        Returns:
            float: The calculated chemiphoretic gradient.
        """
        chemiphoretic_gradient = np.log((ci - cb) / channel_length)
        return chemiphoretic_gradient

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
        beta_potential = (cation - anion) / (cation + anion)
        return beta_potential

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
        reynolds_number = (density * velocity * characteristic_length) / dynamic_viscosity
        return reynolds_number

    # Private methods
    @staticmethod
    def _convert_variables(channel_height, channel_length, mean_flow_velocity, diffusiophoretic_velocity) -> tuple:
        """
        Convert variables to SI units for calculations.
        
        Parameters:
            channel_height (float): Channel height in micrometers.
            channel_length (float): Channel length in centimeters.
            mean_flow_velocity (float): Flow velocity in mm/s.
            diffusiophoretic_velocity (float): Diffusiophoretic velocity in µm/s.

        Returns:
            tuple: Converted values for channel height (m), channel length (m), flow velocity (m/s), 
                   and diffusiophoretic velocity (m/s).
        """
        channel_height *= 10**-6  # µm to meters
        channel_length *= 1       # cm to meters
        mean_flow_velocity *= 10**-3  # mm/s to m/s
        diffusiophoretic_velocity *= 10**-6  # µm/s to m/s

        return channel_height, channel_length, mean_flow_velocity, diffusiophoretic_velocity
    
    @staticmethod
    def _calculate_particle_trajectory(channel_height, channel_length, mean_flow_velocity, diffusiophoretic_velocity) -> tuple:
        """
        Calculates the trajectory of the particles based on the diffusiophoretic velocity and flow.

        Returns:
            tuple: X and Y positions of the particle trajectory as percentages of channel length and height.
        """
        number_of_particles = 1
        number_of_points = 200
        y = np.linspace(start=0, stop=channel_height, num=number_of_particles)  # Particle Y positions
        time = np.linspace(start=0, stop=200, num=number_of_points)             # Time vector (0 to 200 seconds)

        # Calculate particle position
        x_pos, y_pos = DiffusiophoresisFormulas._calculate_particle_position(channel_height,  mean_flow_velocity, diffusiophoretic_velocity, time, y)
        
        # Convert to percentages of the channel's length and height
        x_percentage = (100 * x_pos) / (channel_length * 10**6)
        y_percentage = (100 * y_pos) / (channel_height * 10**6)
        
        return x_percentage, y_percentage
    
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
    def _integrate(x, y) -> float:
        """
        Computes the area under the particle trajectory by integrating the path length.

        Args:
            x (array): X positions of the particle trajectory.
            y (array): Y positions of the particle trajectory.

        Returns:
            float: The integrated area under the trajectory.
        """
        dx = np.diff(x)
        dy = np.diff(y)
        area = np.sum(np.sqrt(dx**2 + dy**2))  # Arc length computation
        return area
