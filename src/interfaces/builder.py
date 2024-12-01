from abc import ABC, abstractmethod

class Builder(ABC):
    """
    Interface for builders that construct complex objects with various configurations.
    
    Methods:
        set_data_broadcaster(data_broadcaster): Abstract method for setting a DataBroadcaster.
        set_progress_analyzer(progress_analyzer): Abstract method for setting a ProgressAnalyzer.
        build(): Abstract method to create and return the fully constructed object.
    """
    
    @abstractmethod
    def build(self):
        pass