from ga.genetic_algorithm import genetic_algorithm
from ga.benchmark.genetic_algorithm_benchmark import GeneticAlgorithmBenchmark
from functions.test_functions.ackley import AckleyTest
from functions.test_functions.rastrigin import RastriginTest
from functions.test_functions.easom import EasomTest
from functions.test_functions.levy import LevyTest
from functions.test_functions.sphere import SphereTest
if __name__ == "__main__":
    #main_coordinator = MainCoordinator()
    #main_coordinator.initialize()

    ackley = AckleyTest()
    rastrigin = RastriginTest()
    easom = EasomTest()
    levy = LevyTest()
    sphere = SphereTest()

    #func, bounds, args = ackley.get_parameters()
    #solution = genetic_algorithm(func, bounds, args,1000,1000)
    #print(solution)

    test_func = [ackley, rastrigin, easom, levy, sphere]

    benchmark = GeneticAlgorithmBenchmark(1000, 100, test_func, 250)
    benchmark.run()