from math_statement import MathStatement

class Logical(MathStatement):

    VALID_TYPES = ["conjunction", "disjunction", "implication", "equivalence"]

    def __init__(self, elements, type):
        super().__init__()
        
        self._elements = []
        self._type = None

        self.elements = elements
        self.type = type

    def _validate_elements(self, value):
        """Validate that elements is a list of MathStatement instances."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Elements must be a list or tuple, got {value} (type: {type(value)})")
        
        if len(value) < 2:
            raise ValueError(f"Elements must have at least 2 items, got {len(value)} items: {value}")
        
        for i, element in enumerate(value):
            if not isinstance(element, MathStatement):
                raise TypeError(f"Element at index {i} must be a MathStatement instance, got {element} (type: {type(element)})")
    
    def _validate_type(self, value):
        """Validate that type is in VALID_TYPES."""
        if value not in self.VALID_TYPES:
            raise ValueError(f"Type must be one of {self.VALID_TYPES}, got {value} (type: {type(value)})")
    
    @property
    def elements(self):
        return self._elements.copy()  # Return a copy to prevent direct modification
    
    @elements.setter
    def elements(self, value):
        self._validate_elements(value)
        self._elements = list(value)  # Convert to list for consistency
    
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, value):
        self._validate_type(value)
        self._type = value
    
    def __str__(self):
        """Return a string representation of the logical statement."""
        op_symbols = {
            "conjunction": " ∧ ",
            "disjunction": " ∨ ",
            "implication": " → ",
            "equivalence": " ↔ "
        }
        op_symbol = op_symbols.get(str(self.type), f" {self.type} ")
        return f"({op_symbol.join(str(elem) for elem in self.elements)})"
    
    def __repr__(self):
        """Return a detailed string representation of the logical statement."""
        return f"Logical({self.elements}, '{self.type}')"