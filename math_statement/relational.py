import sympy as sp
from math_statement import MathStatement

class Relational(MathStatement):

    VALID_OPERATORS = [sp.Eq, sp.Ne, sp.Lt, sp.Le]

    def __init__(self, left, operator, right):
        super().__init__()
        
        self._operator = None
        self._sides = []

        self.operator = operator
        self.sides = [left, right]
    
    def _validate_operator(self, value):
        """Validate that the operator is in VALID_OPERATORS."""
        if value not in self.VALID_OPERATORS:
            raise ValueError(f"Operator must be one of {self.VALID_OPERATORS}, got {value} (type: {type(value)})")
    
    def _validate_sympy_expression(self, value, side_name):
        """Validate that the value is a SymPy expression."""
        if not isinstance(value, sp.Basic):
            raise TypeError(f"{side_name} side must be a SymPy expression, got {value} (type: {type(value)})")
    
    def _validate_sides_container(self, value):
        """Validate that the value is a container with exactly 2 elements."""
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise ValueError(f"Sides must be a list or tuple with exactly 2 elements, got {value} (type: {type(value)})")
    
    @property
    def operator(self):
        return self._operator
    
    @operator.setter
    def operator(self, value):
        self._validate_operator(value)
        self._operator = value
    
    @property
    def left(self):
        return self._sides[0]
    
    @left.setter
    def left(self, value):
        self._validate_sympy_expression(value, "Left")
        self._sides[0] = value
    
    @property
    def right(self):
        return self._sides[1]
    
    @right.setter
    def right(self, value):
        self._validate_sympy_expression(value, "Right")
        self._sides[1] = value
    
    @property
    def sides(self):
        return self._sides.copy()  # Return a copy to prevent direct modification
    
    @sides.setter
    def sides(self, value):
        self._validate_sides_container(value)
        
        left, right = value
        self._validate_sympy_expression(left, "Left")
        self._validate_sympy_expression(right, "Right")
        
        self._sides = [left, right]
    
    def __str__(self):
        """Return a string representation of the relational statement."""
        op_symbols = {sp.Eq: "=", sp.Ne: "≠", sp.Lt: "<", sp.Le: "≤"}
        op_symbol = op_symbols.get(self.operator, str(self.operator))
        return f"{self.left} {op_symbol} {self.right}"
    
    def __repr__(self):
        """Return a detailed string representation of the relational statement."""
        op_names = {sp.Eq: "Eq", sp.Ne: "Ne", sp.Lt: "Lt", sp.Le: "Le"}
        op_name = op_names.get(self.operator, str(self.operator))
        return f"Relational({self.left}, {op_name}, {self.right})"
