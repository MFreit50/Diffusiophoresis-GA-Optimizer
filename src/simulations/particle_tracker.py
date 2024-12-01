# This script simulates the trajectory of particles undergoing diffusiophoresis in a microchannel. 
# It was originally written by Graham Werner in MatLab and has been translated to Python for this example.

import numpy as np
import matplotlib.pyplot as plt

# Parameters
Channel_Height = 250  # in um
Channel_Width = 0.1   # in cm
Mean_Flow_Velocity = 1  # in mm/s
Channel_Length = 0.1   # in meters
Diffusiophoretic_Velocity = 1  # in um/s

# Unit conversions
L = Channel_Length                 # Channel length in meters
W = Channel_Width * 10**-2         # Converts from cm to meters
H = Channel_Height * 10**-6        # Converts from um to meters
V = Mean_Flow_Velocity * 10**-3    # Flow velocity mm/s to m/s
Diffusio_PosTrack = Diffusiophoretic_Velocity * 10**-6  # Diffusiophoretic velocity in m/s

# Particle tracking
Y0_Range = np.linspace(0, H, 50)  # Particles starting at different Y positions (0 to H)
t = np.linspace(0, 200, 101)      # Time vector from 0 to 200 seconds

# Plotting
plt.figure()
for Y0_Val in Y0_Range:
    # Calculate X and Y positions of the particles over time
    X_pos = (10**6 * 6 * V) * (((Diffusio_PosTrack * t**2) / (2 * H)) - 
                               ((Diffusio_PosTrack**2 * t**3) / (3 * H**2)) + 
                               ((Y0_Val * t) / H) - 
                               ((Diffusio_PosTrack * Y0_Val * t**2) / (H**2)) - 
                               ((Y0_Val**2 * t) / (H**2)))  # X position in um

    Y_pos = (Diffusio_PosTrack * t + Y0_Val) * 10**6  # Y position in um
    
    # Convert to percentage of channel length and height
    X_percentage = (100 * X_pos) / (L * 10**6)
    Y_percentage = (100 * Y_pos) / (H * 10**6)
    
    # Plot the particle trajectory
    plt.plot(X_percentage, Y_percentage, linewidth=1)

# Customize plot
plt.xlabel('% Channel Length')
plt.ylabel('% Channel Height')
plt.title('Particle Tracking for Diffusiophoresis')
plt.xlim([0, 100])
plt.ylim([0, 100])
plt.grid(True)
plt.show()
