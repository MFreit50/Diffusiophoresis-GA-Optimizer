import numpy as np
import matplotlib.pyplot as plt

# Define the Rastrigin function
def rastrigin(X, Y, A=10):
    n = 2  # Number of dimensions (in this case X and Y)
    Z = A * n + (X**2 - A * np.cos(2 * np.pi * X)) + (Y**2 - A * np.cos(2 * np.pi * Y))
    return Z

# Create a grid of values for X and Y
x = np.linspace(-5.12, 5.12, 500)
y = np.linspace(-5.12, 5.12, 500)
X, Y = np.meshgrid(x, y)

# Calculate Z values (Rastrigin values) for the grid
Z = rastrigin(X, Y)

# Plot the Rastrigin function as a 3D surface plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

# Labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Rastrigin Value')
ax.set_title('3D Plot of Rastrigin Function')

plt.show()