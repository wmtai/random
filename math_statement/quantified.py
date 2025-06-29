import sympy as sp
from math_statement import MathStatement
from logical import Logical

class Quantified(MathStatement):

    VALID_TYPES = ["universal", "existential"]
    
    def __init__(self, variables, domain, predicate, type):
        super().__init__()
        
        self._variables = []
        self._domain = None
        self._predicate = None
        self._type = None
        
        # Use property setters to enforce validation
        self.variables = variables
        self.domain = domain
        self.predicate = predicate
        self.type = type
    
    def _validate_variables(self, value):
        """Validate that variables is a list of SymPy symbols."""
        if not isinstance(value, (list, tuple)):
            raise TypeError(f"Variables must be a list or tuple, got {value} (type: {type(value)})")
        
        if len(value) == 0:
            raise ValueError(f"Variables list cannot be empty, got {value}")
        
        for i, var in enumerate(value):
            if not isinstance(var, sp.Symbol):
                raise TypeError(f"Variable at index {i} must be a SymPy Symbol, got {var} (type: {type(var)})")
    
    def _validate_math_statement(self, value, name):
        """Validate that value is a MathStatement instance."""
        if not isinstance(value, MathStatement):
            raise TypeError(f"{name} must be a MathStatement instance, got {value} (type: {type(value)})")
    
    def _validate_type(self, value):
        """Validate that type is in VALID_TYPES."""
        if value not in self.VALID_TYPES:
            raise ValueError(f"Type must be one of {self.VALID_TYPES}, got {value} (type: {type(value)})")
    
    @property
    def variables(self):
        return self._variables.copy()  # Return a copy to prevent direct modification
    
    @variables.setter
    def variables(self, value):
        self._validate_variables(value)
        self._variables = list(value)  # Convert to list for consistency
    
    @property
    def domain(self):
        return self._domain
    
    @domain.setter
    def domain(self, value):
        self._validate_math_statement(value, "Domain")
        self._domain = value
        # Validate variable quantification after setting domain
        if self._predicate is not None:
            self._validate_variable_quantification(self._domain, self._predicate)
    
    @property
    def predicate(self):
        return self._predicate
    
    @predicate.setter
    def predicate(self, value):
        self._validate_math_statement(value, "Predicate")
        self._predicate = value
        # Validate variable quantification after setting predicate
        if self._domain is not None:
            self._validate_variable_quantification(self._domain, self._predicate)
    
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, value):
        self._validate_type(value)
        self._type = value
    
    def __str__(self):
        """Return a string representation of the quantified statement."""
        quantifier = "∀" if self.type == "universal" else "∃"
        vars_str = ", ".join(str(var) for var in self.variables)
        return f"{quantifier}{vars_str} ({self.domain} → {self.predicate})"
    
    def __repr__(self):
        """Return a detailed string representation of the quantified statement."""
        return f"Quantified({self.variables}, {self.domain}, {self.predicate}, '{self.type}')"

    def _validate_variable_quantification(self, domain, predicate):
        """Validate that all variables in Relational objects are quantified."""
        from relational import Relational
        from logical import Logical
        
        def collect_variables_from_relational(rel_obj, quantified_in_current_scope):
            """Recursively collect all SymPy variables from a Relational object."""
            variables = set()
            
            if isinstance(rel_obj, Relational):
                # Collect variables from left and right sides
                for side in [rel_obj.left, rel_obj.right]:
                    if hasattr(side, 'free_symbols'):
                        variables.update(side.free_symbols)
            elif isinstance(rel_obj, Logical):
                # Recursively check all elements
                for element in rel_obj.elements:
                    variables.update(collect_variables_from_relational(element, quantified_in_current_scope))
            elif isinstance(rel_obj, Quantified):
                # First, validate that the inner quantified statement is well-formed
                inner_quantified = set(rel_obj.variables)
                inner_domain_vars = collect_variables_from_relational(rel_obj.domain, inner_quantified)
                inner_predicate_vars = collect_variables_from_relational(rel_obj.predicate, inner_quantified)
                inner_all_vars = inner_domain_vars.union(inner_predicate_vars)
                inner_unquantified = inner_all_vars - inner_quantified
                
                if inner_unquantified:
                    var_names = ", ".join(str(var) for var in inner_unquantified)
                    raise ValueError(f"Inner quantified statement has unquantified variables: {var_names}")
                
                # If inner statement is valid, only add variables that are not quantified in the inner scope
                variables.update(inner_all_vars - inner_quantified)
            
            return variables
        
        # Collect all variables from domain and predicate
        all_variables = set()
        all_variables.update(collect_variables_from_relational(domain, set(self._variables)))
        all_variables.update(collect_variables_from_relational(predicate, set(self._variables)))
        
        # Get the set of quantified variables
        quantified_vars = set(self._variables)
        
        # Check if all variables are quantified
        unquantified_vars = all_variables - quantified_vars
        if unquantified_vars:
            var_names = ", ".join(str(var) for var in unquantified_vars)
            raise ValueError(f"All variables in Relational objects must be quantified. Unquantified variables: {var_names}")
