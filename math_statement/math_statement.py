from abc import ABC, abstractmethod

class MathStatement(ABC):
    """
    Abstract base class for mathematical statements.
    
    This class serves as the common interface for Relational, Quantified, and Logical statements.
    All mathematical statement types should inherit from this class.
    """
    
    def __init__(self):
        """Initialize a mathematical statement."""
        pass
    
    @abstractmethod
    def __str__(self):
        """Return a string representation of the statement."""
        pass
    
    @abstractmethod
    def __repr__(self):
        """Return a detailed string representation of the statement."""
        pass
    
    def is_relational(self):
        """Check if this is a relational statement."""
        from relational import Relational
        return isinstance(self, Relational)
    
    def is_quantified(self):
        """Check if this is a quantified statement."""
        from quantified import Quantified
        return isinstance(self, Quantified)
    
    def is_logical(self):
        """Check if this is a logical statement."""
        from logical import Logical
        return isinstance(self, Logical) 