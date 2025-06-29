import pytest
import sympy as sp
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from relational import Relational
from quantified import Quantified
from logical import Logical


class TestVariableQuantification:
    """Test cases for variable quantification validation."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.x = sp.Symbol('x')
        self.y = sp.Symbol('y')
        self.z = sp.Symbol('z')
        
        # Create basic relational statements
        self.rel1 = Relational(self.x, sp.Eq, sp.Integer(5))
        self.rel2 = Relational(self.y, sp.Lt, sp.Integer(10))
        self.rel3 = Relational(self.z, sp.Le, sp.Integer(0))
    
    def test_valid_quantification_single_variable(self):
        """Test that single variable quantification works correctly."""
        # x is quantified, rel1 uses x - should work
        quant = Quantified([self.x], self.rel1, self.rel1, "universal")
        assert quant.variables == [self.x]
        assert quant.domain == self.rel1
        assert quant.predicate == self.rel1
    
    def test_valid_quantification_multiple_variables(self):
        """Test that multiple variable quantification works correctly."""
        # x and y are quantified, rel1 uses x, rel2 uses y - should work
        quant = Quantified([self.x, self.y], self.rel1, self.rel2, "universal")
        assert quant.variables == [self.x, self.y]
    
    def test_invalid_quantification_missing_variable(self):
        """Test that missing variable in quantification raises error."""
        # x is quantified but rel2 uses y - should fail
        with pytest.raises(ValueError, match="All variables in Relational objects must be quantified"):
            Quantified([self.x], self.rel1, self.rel2, "universal")
    
    def test_invalid_quantification_domain_variable(self):
        """Test that missing variable in domain raises error."""
        # x is quantified but rel2 (domain) uses y - should fail
        with pytest.raises(ValueError, match="All variables in Relational objects must be quantified"):
            Quantified([self.x], self.rel2, self.rel1, "universal")
    
    def test_invalid_quantification_predicate_variable(self):
        """Test that missing variable in predicate raises error."""
        # x is quantified but rel2 (predicate) uses y - should fail
        with pytest.raises(ValueError, match="All variables in Relational objects must be quantified"):
            Quantified([self.x], self.rel1, self.rel2, "universal")
    
    def test_valid_quantification_with_logical_statements(self):
        """Test that logical statements with quantified variables work."""
        # Create logical statement with x and y
        logical = Logical([self.rel1, self.rel2], "conjunction")
        
        # x and y are quantified - should work
        quant = Quantified([self.x, self.y], logical, logical, "universal")
        assert quant.variables == [self.x, self.y]
    
    def test_invalid_quantification_with_logical_statements(self):
        """Test that logical statements with unquantified variables fail."""
        # Create logical statement with x and y
        logical = Logical([self.rel1, self.rel2], "conjunction")
        
        # Only x is quantified but logical uses y too - should fail
        with pytest.raises(ValueError, match="All variables in Relational objects must be quantified"):
            Quantified([self.x], logical, logical, "universal")
    
    def test_valid_quantification_with_nested_quantified(self):
        """Test that nested quantified statements work correctly."""
        # Create inner quantified statement
        inner_quant = Quantified([self.y], self.rel2, self.rel2, "existential")
        
        # x is quantified for outer, y is quantified in inner - should work
        outer_quant = Quantified([self.x], self.rel1, inner_quant, "universal")
        assert outer_quant.variables == [self.x]
    
    def test_valid_quantification_with_nested_quantified_different_variables(self):
        """Test that nested quantified statements with different variables work correctly."""
        # Create inner quantified statement with z
        inner_quant = Quantified([self.z], self.rel3, self.rel3, "existential")
        
        # x is quantified for outer, z is quantified in inner - should work
        # This is valid because z is quantified in the inner scope
        outer_quant = Quantified([self.x], self.rel1, inner_quant, "universal")
        assert outer_quant.variables == [self.x]
    
    def test_invalid_quantification_with_nested_quantified_unquantified_variable(self):
        """Test that nested quantified statements with truly unquantified variables fail."""
        # Create inner quantified statement with z, but use y in domain/predicate
        inner_quant = Quantified([self.z], self.rel2, self.rel2, "existential")  # rel2 uses y, not z
        
        # x is quantified for outer, but inner uses y which is not quantified anywhere - should fail
        with pytest.raises(ValueError, match="All variables in Relational objects must be quantified"):
            Quantified([self.x], self.rel1, inner_quant, "universal")
    
    def test_valid_quantification_with_complex_expressions(self):
        """Test that complex SymPy expressions work correctly."""
        # Create complex expression with x
        complex_expr = self.x + sp.sin(self.x)
        rel_complex = Relational(complex_expr, sp.Eq, sp.Integer(0))
        
        # x is quantified - should work
        quant = Quantified([self.x], rel_complex, rel_complex, "universal")
        assert quant.variables == [self.x]
    
    def test_invalid_quantification_with_complex_expressions(self):
        """Test that complex SymPy expressions with unquantified variables fail."""
        # Create complex expression with x and y
        complex_expr = self.x + self.y
        rel_complex = Relational(complex_expr, sp.Eq, sp.Integer(0))
        
        # Only x is quantified but expression uses y too - should fail
        with pytest.raises(ValueError, match="All variables in Relational objects must be quantified"):
            Quantified([self.x], rel_complex, rel_complex, "universal")
    
    def test_quantification_validation_during_initialization(self):
        """Test that validation happens during initialization."""
        # This should fail during initialization
        with pytest.raises(ValueError, match="All variables in Relational objects must be quantified"):
            Quantified([self.x], self.rel1, self.rel2, "universal")
    
    def test_quantification_validation_during_property_setting(self):
        """Test that validation happens when setting properties."""
        # Create valid quantified statement
        quant = Quantified([self.x, self.y], self.rel1, self.rel1, "universal")
        
        # Try to set predicate with unquantified variable - should fail
        with pytest.raises(ValueError, match="All variables in Relational objects must be quantified"):
            quant.predicate = self.rel3  # rel3 uses z which is not quantified


if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"]) 