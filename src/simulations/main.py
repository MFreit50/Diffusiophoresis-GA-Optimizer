from diffusiophoretic_particle_tracker import DiffusiophoreticParticleTracker
def main():
    # Parameters
    Channel_Height = 250  # in um
    Channel_Width = 0.1   # in cm
    Mean_Flow_Velocity = 1  # in mm/s
    Channel_Length = 0.1   # in meters
    Diffusiophoretic_Velocity = 1  # in um/s
    x = DiffusiophoreticParticleTracker(Channel_Height, Channel_Length, Mean_Flow_Velocity, Diffusiophoretic_Velocity)
    x.display_particle_trajectory()
    area = x.calculate_exclusion_zone_area()
    print(area)

if __name__ == "__main__":
    main()