import pytest
import sympy as sp
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from relational import Relational
from quantified import Quantified
from logical import Logical
from math_statement import MathStatement


class TestMathStatementUnifiedInterface:
    """Test cases for the unified MathStatement interface."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.x = sp.Symbol('x')
        self.y = sp.Symbol('y')
        self.z = sp.Symbol('z')
        
        # Create basic relational statements
        self.rel1 = Relational(self.x, sp.Eq, sp.Integer(5))
        self.rel2 = Relational(self.x, sp.Lt, sp.Integer(10))
        self.rel3 = Relational(self.y, sp.Lt, sp.Integer(0))
    
    def test_relational_creation_and_string_representation(self):
        """Test that relational statements can be created and have proper string representation."""
        assert str(self.rel1) == "x = 5"
        assert str(self.rel2) == "x < 10"
        assert str(self.rel3) == "y < 0"
        
        # Test repr
        assert repr(self.rel1) == "Relational(x, Eq, 5)"
    
    def test_logical_creation_and_string_representation(self):
        """Test that logical statements can be created and have proper string representation."""
        logical1 = Logical([self.rel1, self.rel2], "conjunction")
        logical2 = Logical([self.rel2, self.rel3], "disjunction")
        logical3 = Logical([self.rel1, self.rel2], "implication")
        logical4 = Logical([self.rel1, self.rel2], "equivalence")
        
        assert str(logical1) == "(x = 5 ∧ x < 10)"
        assert str(logical2) == "(x < 10 ∨ y < 0)"
        assert str(logical3) == "(x = 5 → x < 10)"
        assert str(logical4) == "(x = 5 ↔ x < 10)"
        
        # Test repr
        assert "Logical" in repr(logical1)
        assert "conjunction" in repr(logical1)
    
    def test_quantified_creation_and_string_representation(self):
        """Test that quantified statements can be created and have proper string representation."""
        quant1 = Quantified([self.x], self.rel1, self.rel2, "universal")
        quant2 = Quantified([self.y], self.rel3, self.rel1, "existential")
        
        assert str(quant1) == "∀x (x = 5 → x < 10)"
        assert str(quant2) == "∃y (y < 0 → x = 5)"
        
        # Test repr
        assert "Quantified" in repr(quant1)
        assert "universal" in repr(quant1)
    
    def test_unified_math_statement_interface(self):
        """Test the unified MathStatement interface."""
        statements = [self.rel1, Logical([self.rel1, self.rel2], "conjunction"), 
                     Quantified([self.x], self.rel1, self.rel2, "universal")]
        
        for stmt in statements:
            # All should be MathStatement instances
            assert isinstance(stmt, MathStatement)
            
            # Test type checking methods
            assert stmt.is_relational() == isinstance(stmt, Relational)
            assert stmt.is_logical() == isinstance(stmt, Logical)
            assert stmt.is_quantified() == isinstance(stmt, Quantified)
    
    def test_complex_nested_structure(self):
        """Test complex nested mathematical statements."""
        # Create nested logical statement
        inner_logical = Logical([self.rel1, self.rel2], "implication")
        quant1 = Quantified([self.x], self.rel1, self.rel2, "universal")
        quant2 = Quantified([self.y], self.rel3, inner_logical, "existential")
        
        complex_stmt = Logical([quant1, inner_logical, quant2], "conjunction")
        
        # Should be a valid MathStatement
        assert isinstance(complex_stmt, MathStatement)
        assert complex_stmt.is_logical()
        
        # Should have proper string representation
        assert "∧" in str(complex_stmt)
        assert "∀" in str(complex_stmt)
        assert "∃" in str(complex_stmt)
    
    def test_validation_examples(self):
        """Test validation examples from the original example."""
        # Valid logical statement should work
        valid_logical = Logical([self.rel1, self.rel2], "conjunction")
        assert isinstance(valid_logical, MathStatement)
        assert valid_logical.is_logical()
        
        # Invalid type should raise ValueError
        with pytest.raises(ValueError, match="Type must be one of"):
            Logical([self.rel1, self.rel2], "invalid_type")
        
        # Not enough elements should raise ValueError
        with pytest.raises(ValueError, match="Elements must have at least 2 items"):
            Logical([self.rel1], "conjunction")
    
    def test_property_access_and_modification(self):
        """Test property access and modification for all statement types."""
        # Test relational properties
        assert self.rel1.left == self.x
        assert self.rel1.right == sp.Integer(5)
        assert self.rel1.operator == sp.Eq
        
        # Modify relational properties
        self.rel1.left = self.y
        assert self.rel1.left == self.y
        assert str(self.rel1) == "y = 5"
        
        # Test logical properties
        logical = Logical([self.rel1, self.rel2], "conjunction")
        assert logical.type == "conjunction"
        assert len(logical.elements) == 2
        
        # Modify logical properties
        logical.type = "disjunction"
        assert logical.type == "disjunction"
        assert str(logical) == "(y = 5 ∨ x < 10)"
        
        # Test quantified properties
        quant = Quantified([self.x], self.rel1, self.rel2, "universal")
        assert quant.type == "universal"
        assert len(quant.variables) == 1
        assert quant.variables[0] == self.x
        
        # Modify quantified properties
        quant.type = "existential"
        assert quant.type == "existential"
        assert str(quant) == "∃x (y = 5 → x < 10)"
    
    def test_validation_error_messages(self):
        """Test that validation error messages include the actual values."""
        # Test operator error message
        with pytest.raises(ValueError) as exc_info:
            Relational(self.x, "invalid_op", sp.Integer(5))
        assert "invalid_op" in str(exc_info.value)
        assert "type: <class 'str'>" in str(exc_info.value)
        
        # Test variables error message
        with pytest.raises(TypeError) as exc_info:
            Quantified(["not_a_symbol"], self.rel1, self.rel2, "universal")
        assert "not_a_symbol" in str(exc_info.value)
        assert "type: <class 'str'>" in str(exc_info.value)
        
        # Test elements error message
        with pytest.raises(TypeError) as exc_info:
            Logical([self.rel1, "not_a_statement"], "conjunction")
        assert "not_a_statement" in str(exc_info.value)
        assert "type: <class 'str'>" in str(exc_info.value)
    
    def test_defensive_copying(self):
        """Test that property getters return copies to prevent direct modification."""
        # Test relational sides
        sides = self.rel1.sides
        sides[0] = self.y
        assert self.rel1.left == self.x  # Should be unchanged
        
        # Test logical elements
        logical = Logical([self.rel1, self.rel2], "conjunction")
        elements = logical.elements
        elements[0] = self.rel3
        assert logical.elements[0] == self.rel1  # Should be unchanged
        
        # Test quantified variables
        quant = Quantified([self.x, self.y], self.rel1, self.rel2, "universal")
        variables = quant.variables
        variables[0] = self.z
        assert quant.variables[0] == self.x  # Should be unchanged
    
    def test_all_valid_operators_and_types(self):
        """Test all valid operators and types work correctly."""
        # Test all relational operators
        operators = [sp.Eq, sp.Ne, sp.Lt, sp.Le]
        for op in operators:
            rel = Relational(self.x, op, sp.Integer(5))
            assert rel.operator == op
        
        # Test all logical types
        logical_types = ["conjunction", "disjunction", "implication", "equivalence"]
        for ltype in logical_types:
            logical = Logical([self.rel1, self.rel2], ltype)
            assert logical.type == ltype
        
        # Test all quantified types
        quant_types = ["universal", "existential"]
        for qtype in quant_types:
            quant = Quantified([self.x], self.rel1, self.rel2, qtype)
            assert quant.type == qtype
    
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
        
        # Test with integrals
        integral = sp.integrate(expr1, self.x)
        rel.right = integral
        assert rel.right == integral
    
    def test_multiple_variables_in_quantified(self):
        """Test quantified statements with multiple variables."""
        variables = [self.x, self.y, self.z]
        quant = Quantified(variables, self.rel1, self.rel2, "universal")
        
        assert len(quant.variables) == 3
        assert quant.variables == [self.x, self.y, self.z]
        assert "∀x, y, z" in str(quant)
    
    def test_empty_variables_list_validation(self):
        """Test that empty variables list is properly validated."""
        with pytest.raises(ValueError, match="Variables list cannot be empty"):
            Quantified([], self.rel1, self.rel2, "universal")
    
    def test_invalid_variable_type_validation(self):
        """Test that invalid variable types are properly validated."""
        invalid_variables = [5, "x", None, [1, 2], {"key": "value"}]
        for var in invalid_variables:
            with pytest.raises(TypeError, match="must be a SymPy Symbol"):
                Quantified([var], self.rel1, self.rel2, "universal")


if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"]) 