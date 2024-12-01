from ga.strategy_manager import StrategyManager
from ga.data_aggregator import DataAggregator
from Modules.data_broadcaster import DataBroadcaster
from ga.progress_analyzer import ProgressAnalyzer
from ga.genetic_algorithm import GeneticAlgorithm
from interfaces.builder import Builder

class GeneticAlgorithmBuilder(Builder):
    """
    Builder class to create and configure a GeneticAlgorithm instance with optional data aggregation capabilities.

    Attributes:
        generations (int): Number of generations for the genetic algorithm to run.
        population_size (int): Size of the population for each generation.
        strategy_manager (StrategyManager): Manager for the strategy configurations used in the algorithm.
        data_aggregator (DataAggregator): Aggregates data using a ProgressAnalyzer and DataBroadcaster.
    """

    def __init__(self, generations: int, population_size: int):
        """
        Initializes the GeneticAlgorithmBuilder with the specified parameters.

        Args:
            generations (int): Number of generations for the genetic algorithm.
            population_size (int): Size of the population in each generation.
        """
        # Genetic Algorithm parameters
        self.generations = generations
        self.population_size = population_size

        # Initialize Strategy Manager
        self.strategy_manager = StrategyManager()

        # Initialize Data Aggregator with ProgressAnalyzer and DataBroadcaster
        progress_analyzer: ProgressAnalyzer = ProgressAnalyzer()
        data_broadcaster: DataBroadcaster = DataBroadcaster()
        self.data_aggregator = DataAggregator(data_broadcaster, progress_analyzer)

    def build(self, include_data_aggregator: bool = True) -> GeneticAlgorithm:
        """
        Builds and returns a GeneticAlgorithm instance, optionally including the DataAggregator.

        Args:
            include_data_aggregator (bool): If True, the DataAggregator is included in the GeneticAlgorithm instance.

        Returns:
            GeneticAlgorithm: Configured GeneticAlgorithm instance.
        """
        genetic_algorithm: GeneticAlgorithm
        if not include_data_aggregator:
            # Create GeneticAlgorithm without data aggregation
            genetic_algorithm = GeneticAlgorithm(
                self.generations, 
                self.population_size, 
                self.strategy_manager
            )
        else:
            # Create GeneticAlgorithm with data aggregation
            genetic_algorithm = GeneticAlgorithm(
                self.generations, 
                self.population_size, 
                self.strategy_manager, 
                self.data_aggregator
            )
        
        return genetic_algorithm