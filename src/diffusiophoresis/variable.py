import numpy as np

class Variable:
    """
    A class to represent a variable with a name, value, range, and constant state.

    Attributes
    ----------
    variable_name : str
        The name of the variable.
    value : float
        The current value of the variable.
    is_constant : bool
        Determines if the variable is constant. If True, its value cannot be changed.
    min_range : float
        The minimum allowed value for the variable.
    max_range : float
        The maximum allowed value for the variable.

    Methods
    -------
    get_name():
        Returns the name of the variable.

    set_value(value, safe_mode=False):
        Sets a new value for the variable if it is not constant. 
        In safe mode, raises an error if trying to change a constant variable.

    randomize():
        Randomly assigns a value to the variable within its range if it is not constant.

    is_within_range(value):
        Checks if the given value is within the variable's range.
    """

    def __init__(self, variable_name: str, value: float, is_constant: bool, min_range: float, max_range: float) -> None:
        """
        Constructs a new 'Variable' instance.

        Parameters
        ----------
        variable_name : str
            The name of the variable.
        value : float
            The initial value of the variable.
        is_constant : bool
            Specifies whether the variable is constant.
        min_range : float
            The minimum allowed value for the variable.
        max_range : float
            The maximum allowed value for the variable.
        """
        self.variable_name = variable_name
        self.value = value
        self.is_constant = is_constant
        self.min_range = min_range
        self.max_range = max_range

    def get_name(self):
        """
        Returns the name of the variable.

        Returns
        -------
        str
            The name of the variable.
        """
        return self.variable_name
    
    def set_value(self, value: float, safe_mode: bool = False):
        """
        Sets the value of the variable if it's not constant.
        If 'safe_mode' is enabled, raises an error if attempting to change a constant variable.

        Parameters
        ----------
        value : float
            The new value to set.
        safe_mode : bool, optional
            If True, raises an exception when trying to set a value for a constant variable (default is False).

        Raises
        ------
        ValueError
            If trying to change the value of a constant variable in safe mode.
        """
        if self.is_constant:
            if safe_mode:
                raise ValueError(f"Variable '{self.variable_name}' is constant and cannot be reassigned")
            return  # Do not set value of a constant variable
        self.value = value

    def randomize(self) -> None:
        """
        Randomly assigns a value within the variable's range if it is not constant.

        The value is generated using a uniform distribution between the minimum and maximum range.
        """
        if not self.is_constant:
            self.value = np.random.uniform(self.min_range, self.max_range)
    
    def is_within_range(self, value: float) -> bool:
        """
        Checks whether a given value is within the variable's defined range.

        Parameters
        ----------
        value : float
            The value to check.

        Returns
        -------
        bool
            True if the value is within the range [min_range, max_range], False otherwise.
        """
        return self.min_range <= value <= self.max_range