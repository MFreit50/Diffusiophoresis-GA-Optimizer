import numpy as np

class Variable:
    """
    A class to represent a variable with a name, value, range, and constant state.

    Attributes
    ----------
    _variable_name : str
        The name of the variable.
    _value : float
        The current value of the variable.
    _is_constant : bool
        Determines if the variable is constant. If True, its value cannot be changed.
    _min_range : float
        The minimum allowed value for the variable.
    _max_range : float
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
        _variable_name : str
            The name of the variable.
        _value : float
            The initial value of the variable.
        _is_constant : bool
            Specifies whether the variable is constant.
        _min_range : float
            The minimum allowed value for the variable.
        _max_range : float
            The maximum allowed value for the variable.
        """
        self._variable_name = variable_name
        self._value = value
        self._is_constant = is_constant
        self._min_range = min_range
        self._max_range = max_range



    ##Accessor Methods
    def get_name(self) -> str:
        """
        Returns the name of the variable.

        Returns
        -------
        str
            The name of the variable.
        """
        return self._variable_name
    
    def get_value(self) -> float:
        return self._value
    
    def get_min_range(self) -> float:
        """
        Returns the minimum range of the variable.

        Returns
        -------
        float
            The minimum allowed value for the variable.
        """
        return self._min_range

    def get_max_range(self) -> float:
        """
        Returns the maximum range of the variable.

        Returns
        -------
        float
            The maximum allowed value for the variable.
        """
        return self._max_range

    def is_constant(self) -> bool:
        """
        Returns whether the variable is constant.

        Returns
        -------
        bool
            True if the variable is constant, False otherwise.
        """
        return self._is_constant



    ##Mutator Methods
    def set_value(self, value: float, safe_mode: bool = False) -> None:
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
        if self._is_constant:
            if safe_mode:
                raise ValueError(f"Variable '{self._variable_name}' is constant and cannot be reassigned")
            return  # Do not set value of a constant variable
        self._value = value

    def set_min_range(self, min_range: float) -> None:
        """
        Sets the minimum range of the variable.

        Parameters
        ----------
        min_range : float
            The new minimum value for the variable's range.
        """
        self._min_range = min_range

    def set_max_range(self, max_range: float) -> None:
        """
        Sets the maximum range of the variable.

        Parameters
        ----------
        max_range : float
            The new maximum value for the variable's range.
        """
        self._max_range = max_range

    def set_constant(self, is_constant: bool) -> None:
        """
        Sets whether the variable is constant.

        Parameters
        ----------
        is_constant : bool
            True to make the variable constant, False otherwise.
        """
        self._is_constant = is_constant



    ##Utility Methods
    def randomize(self) -> None:
        """
        Randomly assigns a value within the variable's range if it is not constant.

        The value is generated using a uniform distribution between the minimum and maximum range.
        """
        if not self._is_constant:
            self._value = np.random.uniform(self._min_range, self._max_range)
    
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
        return self._min_range <= value <= self._max_range
    


    ##Magic Methods
    def __hash__(self) -> int:
        return hash( (self._variable_name, self._value, self._is_constant, self._min_range, self._max_range) )

    def __eq__(self, other) -> int:
        if isinstance(other, Variable):
            return self._variable_name == other._variable_name and self._value == other._value and self._is_constant == other._is_constant and self._min_range == other._min_range and self._max_range == other._max_range
    
    def __str__(self):
        """
        Returns a string representation of the Variable object.

        Returns
        -------
        str
            A string describing the variable's name, value, constant state, and range.
        """
        constant_status = "Constant" if self._is_constant else "Variable"
        return f"{self._variable_name}: {self._value} [{self._min_range}, {self._max_range}] ({constant_status})"    



    ##Serialization Methods
    def to_dict(self) -> dict:
        """
        Converts the Variable object to a dictionary representation.

        Returns
        -------
        dict
            A dictionary containing the variable's name, value, constant state, 
            and range (min_range, max_range).
        """
        return {
            "variable_name": self._variable_name,
            "value": self._value,
            "is_constant": self._is_constant,
            "min_range": self._min_range,
            "max_range": self._max_range
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a Variable object from a dictionary representation.

        Parameters
        ----------
        data : dict
            A dictionary containing the variable's name, value, constant state, 
            and range (min_range, max_range).

        Returns
        -------
        Variable
            A Variable object initialized with the values from the dictionary.
        """
        return cls(
            _variable_name=data["variable_name"],
            _value=data["value"],
            _is_constant=data["is_constant"],
            _min_range=data["min_range"],
            _max_range=data["max_range"]
        )