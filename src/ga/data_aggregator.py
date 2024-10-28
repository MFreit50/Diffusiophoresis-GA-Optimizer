from Modules.data_broadcaster import DataBroadcaster
from ga.progress_analyzer import ProgressAnalyzer
class DataAggregator():
    def __init__(self, data_broadcaster, progress_analyzer):
        self.data_log = {}
        self.data_broadcaster : DataBroadcaster = data_broadcaster
        self.progress_analyzer : ProgressAnalyzer = progress_analyzer

    def get_log(self):
        return self.data_log
    
    def get(self, component_name : str):
        if component_name not in self.data_log:
            raise KeyError(f"Value '{component_name}' not found in DataAggregator")
        
        return self.data_log[component_name]
    
    def log(self, component_name : str, data : any):
        self.data_log[component_name] = data

    def log_dict(self, dictionary : dict):
        self.data_log.update(dictionary)
    
    def subscribe(self, subscriber):
        self.data_broadcaster.subscribe(subscriber)

    def broadcast_data(self, clear_data_after_broadcast = False):
        self.data_broadcaster.broadcast(self.data_log)

        if clear_data_after_broadcast == True:
            self.data_log.clear()
    
    def analyze_genetic_algorithm(self, population, fitness_scores):
        data = self.progress_analyzer.analyze(population, fitness_scores)
        self.log_dict(data)
    
    def __str__(self):
        output = []
        for key, value in self.data_log.items():
            output.append(f"{key}: {value}")
        return "\n".join(output) + "\n"