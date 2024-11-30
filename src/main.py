from Modules.main_coordinator import MainCoordinator
from ga.genetic_algorithm import genetic_algorithm
if __name__ == "__main__":
    #main_coordinator = MainCoordinator()
    #main_coordinator.initialize()

        
    def sphere(x):
        return -(x[0]**2 + x[1]**2 + x[2]**2 + x[3]**2 + x[4]**2)
    
    bounds = [(-5,5)]*5
    a= sphere
    solution = genetic_algorithm(a, bounds,None,1000,15)
    print(solution)