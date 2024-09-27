import numpy as np
class Variable():
    def __init__(self, value : float, is_constant, min_range, max_range, variable_name) -> None:
        self.value = value
        self.is_constant = is_constant
        self.min_range = min_range
        max_range = max_range
        self.variable_name = variable_name

    def randomize(self) -> None:
        if not self.is_constant:
            self.value = np.random.rand(self.min_range, self.max_range)
    
    def _is_within_range(self, value) -> bool:
        return (value >= self.min_range and value <= self.max_range)