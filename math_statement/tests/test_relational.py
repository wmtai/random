import pytest
import sympy as sp
import sys
import os

# Add the parent directory to the path so we can import the relational module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from relational import Relational


class TestRelational:
    """Test cases for the Relational class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.x = sp.Symbol('x')
        self.y = sp.Symbol('y')
        self.five = sp.Integer(5)
        self.ten = sp.Integer(10)
    
    def test_valid_initialization(self):
        """Test that Relational can be initialized with valid arguments."""
        rel = Relational(self.x, sp.Eq, self.five)
        assert rel.operator == sp.Eq
        assert rel.left == self.x
        assert rel.right == self.five
        assert rel.sides == [self.x, self.five]
    
    def test_all_valid_operators(self):
        """Test that all valid operators work correctly."""
        operators = [sp.Eq, sp.Ne, sp.Lt, sp.Le]
        for op in operators:
            rel = Relational(self.x, op, self.five)
            assert rel.operator == op
    
    def test_invalid_operator_initialization(self):
        """Test that invalid operators raise ValueError during initialization."""
        invalid_operators = ["==", "!=", "<", "<=", 5, None, sp.Gt, sp.Ge]
        for op in invalid_operators:
            with pytest.raises(ValueError, match="Operator must be one of"):
                Relational(self.x, op, self.five)
    
    def test_invalid_left_side_initialization(self):
        """Test that invalid left side raises TypeError during initialization."""
        invalid_lefts = ["x", 5, None, [1, 2], {"key": "value"}]
        for left in invalid_lefts:
            with pytest.raises(TypeError, match="Left side must be a SymPy expression"):
                Relational(left, sp.Eq, self.five)
    
    def test_invalid_right_side_initialization(self):
        """Test that invalid right side raises TypeError during initialization."""
        invalid_rights = ["5", "y", None, [1, 2], {"key": "value"}]
        for right in invalid_rights:
            with pytest.raises(TypeError, match="Right side must be a SymPy expression"):
                Relational(self.x, sp.Eq, right)
    
    def test_operator_property_setter(self):
        """Test that operator property setter works correctly."""
        rel = Relational(self.x, sp.Eq, self.five)
        
        # Test valid operator changes
        rel.operator = sp.Ne
        assert rel.operator == sp.Ne
        
        rel.operator = sp.Lt
        assert rel.operator == sp.Lt
        
        # Test invalid operator
        with pytest.raises(ValueError, match="Operator must be one of"):
            rel.operator = "invalid"
    
    def test_left_property_setter(self):
        """Test that left property setter works correctly."""
        rel = Relational(self.x, sp.Eq, self.five)
        
        # Test valid left side changes
        rel.left = self.y
        assert rel.left == self.y
        assert rel.sides == [self.y, self.five]
        
        rel.left = sp.Symbol('z')
        assert rel.left == sp.Symbol('z')
        
        # Test invalid left side
        with pytest.raises(TypeError, match="Left side must be a SymPy expression"):
            rel.left = "invalid"
    
    def test_right_property_setter(self):
        """Test that right property setter works correctly."""
        rel = Relational(self.x, sp.Eq, self.five)
        
        # Test valid right side changes
        rel.right = self.ten
        assert rel.right == self.ten
        assert rel.sides == [self.x, self.ten]
        
        rel.right = sp.Symbol('z')
        assert rel.right == sp.Symbol('z')
        
        # Test invalid right side
        with pytest.raises(TypeError, match="Right side must be a SymPy expression"):
            rel.right = "invalid"
    
    def test_sides_property_setter(self):
        """Test that sides property setter works correctly."""
        rel = Relational(self.x, sp.Eq, self.five)
        
        # Test valid sides changes
        new_sides = [self.y, self.ten]
        rel.sides = new_sides
        assert rel.left == self.y
        assert rel.right == self.ten
        assert rel.sides == [self.y, self.ten]
        
        # Test with tuple
        rel.sides = (sp.Symbol('a'), sp.Symbol('b'))
        assert rel.left == sp.Symbol('a')
        assert rel.right == sp.Symbol('b')
        
        # Test invalid container type
        with pytest.raises(ValueError, match="Sides must be a list or tuple"):
            rel.sides = "invalid"
        
        # Test wrong number of elements
        with pytest.raises(ValueError, match="Sides must be a list or tuple"):
            rel.sides = [self.x]  # Only one element
        
        with pytest.raises(ValueError, match="Sides must be a list or tuple"):
            rel.sides = [self.x, self.y, self.five]  # Three elements
        
        # Test invalid elements in sides
        with pytest.raises(TypeError, match="Left side must be a SymPy expression"):
            rel.sides = ["invalid", self.five]
        
        with pytest.raises(TypeError, match="Right side must be a SymPy expression"):
            rel.sides = [self.x, "invalid"]
    
    def test_sides_property_getter_returns_copy(self):
        """Test that sides property getter returns a copy, not the original list."""
        rel = Relational(self.x, sp.Eq, self.five)
        sides = rel.sides
        
        # Modifying the returned list should not affect the original
        sides[0] = self.y
        assert rel.left == self.x  # Should still be x, not y
        assert rel.sides == [self.x, self.five]  # Should be unchanged
    
    def test_complex_sympy_expressions(self):
        """Test that complex SymPy expressions work correctly."""
        # Test with mathematical expressions
        expr1 = self.x + self.y
        expr2 = sp.sin(self.x) * sp.cos(self.y)
        
        rel = Relational(expr1, sp.Eq, expr2)
        assert rel.left == expr1
        assert rel.right == expr2
        
        # Test with derivatives
        deriv = sp.diff(expr1, self.x)
        rel.left = deriv
        assert rel.left == deriv
    
    def test_multiple_assignments(self):
        """Test that multiple property assignments work correctly."""
        rel = Relational(self.x, sp.Eq, self.five)
        
        # Change all properties
        rel.operator = sp.Lt
        rel.left = self.y
        rel.right = self.ten
        
        assert rel.operator == sp.Lt
        assert rel.left == self.y
        assert rel.right == self.ten
        assert rel.sides == [self.y, self.ten]
    
    def test_error_messages_include_values(self):
        """Test that error messages include the actual values that caused the error."""
        # Test operator error message
        with pytest.raises(ValueError) as exc_info:
            Relational(self.x, "invalid_op", self.five)
        assert "invalid_op" in str(exc_info.value)
        assert "type: <class 'str'>" in str(exc_info.value)
        
        # Test left side error message
        with pytest.raises(TypeError) as exc_info:
            Relational("invalid_left", sp.Eq, self.five)
        assert "invalid_left" in str(exc_info.value)
        assert "type: <class 'str'>" in str(exc_info.value)
        
        # Test right side error message
        with pytest.raises(TypeError) as exc_info:
            Relational(self.x, sp.Eq, 123)
        assert "123" in str(exc_info.value)
        assert "type: <class 'int'>" in str(exc_info.value)


if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"]) 