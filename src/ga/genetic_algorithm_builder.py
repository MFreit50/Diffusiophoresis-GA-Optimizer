from ga.strategy_manager import StrategyManager
from ga.data_aggregator import DataAggregator
from ga.data_broadcaster import DataBroadcaster
from ga.progress_analyzer import ProgressAnalyzer
from ga.genetic_algorithm import GeneticAlgorithm

class GeneticAlgorithmBuilder():
    def __init__(self, generations, population_size):
        #Genetic Algorithm
        self.generations = generations
        self.population_size = population_size

        #Strategy Manager
        self.strategy_manager = StrategyManager()

        #Data Aggregator
        progress_analyzer: ProgressAnalyzer = ProgressAnalyzer()
        data_broadcaster: DataBroadcaster = DataBroadcaster()
        self.data_aggregator = DataAggregator(data_broadcaster, progress_analyzer)

    def build(self, include_data_aggregator = True):
        genetic_algorithm : GeneticAlgorithm
        if include_data_aggregator == False:
            genetic_algorithm = GeneticAlgorithm(self.generations, self.population_size, self.strategy_manager)
        else:
            genetic_algorithm = GeneticAlgorithm(self.generations, self.population_size, self.strategy_manager, self.data_aggregator)
        
        return genetic_algorithm