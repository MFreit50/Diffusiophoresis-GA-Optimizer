import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def levy_function(x, y):
    """
    Computes the Levy function for given x and y coordinates.

    Parameters:
    - x: x coordinate
    - y: y coordinate

    Returns:
    - The computed value of the Levy function.
    """
    w1 = 1 + (x + 1) / 4
    w2 = 1 + (y + 1) / 4
    term1 = np.sin(np.pi * w1) ** 2
    term2 = (w2 - 1) ** 2 * (1 + 10 * np.sin(np.pi * w2 + 1) ** 2)
    term3 = (w2 - 1) ** 2 * (1 + np.sin(2 * np.pi * w2) ** 2)
    return term1 + term2 + term3

# Create a grid of x and y values
x = np.linspace(-10, 10, 400)
y = np.linspace(-10, 10, 400)
x, y = np.meshgrid(x, y)

# Compute the function values
z = levy_function(x, y)

# Create a 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis', alpha=0.8)

# Set labels
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('f(x, y)')
ax.set_title('3D Visualization of the Levy Function')

plt.show()