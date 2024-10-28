from Modules.data_broadcaster import DataBroadcaster
from ga.progress_analyzer import ProgressAnalyzer

class DataAggregator:
    """
    Aggregates and manages data for analysis and broadcasting within a genetic algorithm.
    
    Attributes:
        data_log (dict): A dictionary to store logged data for tracking progress and performance metrics.
        data_broadcaster (DataBroadcaster): Instance responsible for managing subscribers and broadcasting data updates.
        progress_analyzer (ProgressAnalyzer): Analyzes the progress of the genetic algorithm based on population and fitness scores.
    """

    def __init__(self, data_broadcaster: DataBroadcaster, progress_analyzer: ProgressAnalyzer):
        """
        Initializes the DataAggregator with a DataBroadcaster and ProgressAnalyzer.

        Args:
            data_broadcaster (DataBroadcaster): Handles broadcasting data to subscribers.
            progress_analyzer (ProgressAnalyzer): Provides methods for analyzing genetic algorithm progress.
        """
        self.data_log = {}
        self.data_broadcaster: DataBroadcaster = data_broadcaster
        self.progress_analyzer: ProgressAnalyzer = progress_analyzer

    def get_log(self) -> dict:
        """
        Retrieves the complete data log.

        Returns:
            dict: The current state of data_log.
        """
        return self.data_log
    
    def get(self, component_name: str):
        """
        Retrieves a specific component's data from the log.

        Args:
            component_name (str): The name of the component to retrieve.

        Returns:
            Any: The data associated with the specified component.

        Raises:
            KeyError: If the component_name is not found in the log.
        """
        if component_name not in self.data_log:
            raise KeyError(f"Value '{component_name}' not found in DataAggregator")
        
        return self.data_log[component_name]
    
    def log(self, component_name: str, data: any):
        """
        Logs data under a specific component name.

        Args:
            component_name (str): The name of the component for which data is being logged.
            data (Any): The data to be stored.
        """
        self.data_log[component_name] = data

    def log_dict(self, dictionary: dict):
        """
        Merges an entire dictionary of data into the data log.

        Args:
            dictionary (dict): Dictionary containing multiple key-value pairs to add to the log.
        """
        self.data_log.update(dictionary)
    
    def subscribe(self, subscriber):
        """
        Adds a subscriber to the DataBroadcaster to receive broadcast updates.

        Args:
            subscriber: The object subscribing to receive data broadcasts.
        """
        self.data_broadcaster.subscribe(subscriber)

    def broadcast_data(self, clear_data_after_broadcast: bool = False):
        """
        Broadcasts the current data log to all subscribers.

        Args:
            clear_data_after_broadcast (bool): If True, clears the data_log after broadcasting.
        """
        self.data_broadcaster.broadcast(self.data_log)

        if clear_data_after_broadcast:
            self.data_log.clear()
    
    def analyze_genetic_algorithm(self, population, fitness_scores):
        """
        Analyzes the progress of the genetic algorithm, logs the analysis results.

        Args:
            population: The current population of individuals.
            fitness_scores: Fitness scores of the current population.
        """
        data = self.progress_analyzer.analyze(population, fitness_scores)
        self.log_dict(data)
    
    def __str__(self) -> str:
        """
        Generates a string representation of the data log, displaying each component and its logged data.

        Returns:
            str: Formatted string of data log entries.
        """
        output = [f"{key}: {value}" for key, value in self.data_log.items()]
        return "\n".join(output) + "\n"