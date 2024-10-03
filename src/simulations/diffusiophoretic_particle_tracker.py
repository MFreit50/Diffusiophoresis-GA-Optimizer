import numpy as np
import matplotlib.pyplot as plt

class DiffusiophoreticParticleTracker:
    """
    Originally written by Graham Werner in MatLab and has been translated to Python for this example.
    
    This class models the movement of particles in a fluid using diffusiophoresis.
    It tracks particle trajectories, calculates the exclusion zone area, and 
    displays the particle paths based on input parameters like channel height,
    channel length, flow velocity, and diffusiophoretic velocity.

    Attributes:
        channel_height (float): Height of the channel in micrometers (um).
        channel_length (float): Length of the channel in centimeters (cm).
        mean_flow_velocity (float): Mean flow velocity in millimeters per second (mm/s).
        diffusiophoretic_velocity (float): Diffusiophoretic velocity in micrometers per second (um/s).
    """

    def calculate_exclusion_zone_area(self, channel_height, channel_length, mean_flow_velocity, diffusiophoretic_velocity) -> float:
        """
        Calculates the particle trajectory through exclusion zone and then
        calculates the exclusion zone area by integrating the particle trajectory.

        h = channel_height
        l = channel_length
        v = mean_flow_velocity
        u = diffusiophoretic_velocity

        Returns:
            float: The total exclusion zone area.
        """
        h, l, v, u = self._convert_variables(channel_height, channel_length, mean_flow_velocity, diffusiophoretic_velocity)
        x_percentage, y_percentage = self.calculate_particle_trajectory(h, l, v, u)
        exclusion_zone_area = self._integrate(x_percentage, y_percentage)
        return exclusion_zone_area

    def calculate_particle_trajectory(self, channel_height, channel_length, mean_flow_velocity, diffusiophoretic_velocity) -> tuple:
        """
        Calculates the trajectory of the particles based on the diffusiophoretic velocity and flow.

        Returns:
            tuple: X and Y positions of the particle trajectory as percentages of channel length and height.
        """
        number_of_particles = 1
        number_of_points = 200
        y = np.linspace(start=0, stop=channel_height, num=number_of_particles)  # Particle Y positions
        time = np.linspace(start=0, stop=200, num=number_of_points)                  # Time vector (0 to 200 seconds)

        # Calculate particle position
        x_pos, y_pos = self._calculate_particle_position(channel_height,  mean_flow_velocity, diffusiophoretic_velocity, time, y)
        
        # Convert to percentages of the channel's length and height
        x_percentage = (100 * x_pos) / (channel_length * 10**6)
        y_percentage = (100 * y_pos) / (channel_height * 10**6)
        
        return x_percentage, y_percentage

    def _calculate_particle_position(self, h, v, u, t, y) -> tuple:
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

    def _integrate(self, x, y) -> float:
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

    def display_particle_trajectory(self) -> None:
        """
        Plots and displays the particle trajectory in a 2D plot where X is % of channel length
        and Y is % of channel height.
        """
        plt.figure()

        # Get the particle trajectory
        x_percentage, y_percentage = self.calculate_particle_trajectory()

        # Plot the trajectory
        plt.plot(x_percentage, y_percentage, linewidth=1)
        
        # Customize plot
        plt.xlabel('% Channel Length')
        plt.ylabel('% Channel Height')
        plt.title('Particle Tracking for Diffusiophoresis')
        plt.xlim([0, 100])
        plt.ylim([0, 100])
        plt.grid(True)
        plt.show()

    def _convert_variables(self, channel_height, channel_length, mean_flow_velocity, diffusiophoretic_velocity) -> None:
        """
        Converts the units of channel height, channel length, mean flow velocity,
        and diffusiophoretic velocity to SI units (meters and meters per second).
        """
        channel_height *= 10**-6                                # um to meters
        channel_length *= 1                                     # cm to meters
        mean_flow_velocity *= 10**-3                            # mm/s to m/s
        diffusiophoretic_velocity *= 10**-6                     # um/s to m/s

        return channel_height, channel_length, mean_flow_velocity, diffusiophoretic_velocity