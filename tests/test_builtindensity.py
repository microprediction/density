import pytest
from pydantic import ValidationError
from density.schemachecker.builtindensity import BuiltinDensity

@pytest.mark.parametrize("name,params", [
    ("norm", {"loc": 0.0, "scale": 1.0}),
    ("lognorm", {"s": 0.5, "loc": 0.0, "scale": 1.0}),
    ("expon", {"loc": 0.0, "scale": 1.0}),
    ("t", {"df": 5, "loc": 0.0, "scale": 1.0}),
    ("weibull_min", {"c": 1.5, "loc": 0.0, "scale": 1.0}),
    ("gamma", {"a": 2.0, "loc": 0.0, "scale": 1.0}),
    ("weibull_max", {"c": 2.0, "loc": 0.0, "scale": 1.0}),
    ("beta", {"a": 2.0, "b": 5.0, "loc": 0.0, "scale": 1.0}),
    ("chi", {"df": 3, "loc": 0.0, "scale": 1.0}),
    ("chi2", {"df": 4, "loc": 0.0, "scale": 1.0}),
    ("rayleigh", {"loc": 0.0, "scale": 1.0}),
    ("pareto", {"b": 2.5, "loc": 0.0, "scale": 1.0}),
    ("cauchy", {"loc": 0.0, "scale": 1.0}),
    ("laplace", {"loc": 0.0, "scale": 1.0}),
    ("f", {"dfn": 3, "dfd": 5, "loc": 0.0, "scale": 1.0}),
])
def test_valid_builtin_distributions(name, params):
    """Test that BuiltinDensity accepts various valid distributions."""
    bd = BuiltinDensity(type="builtin", name=name, params=params)
    assert bd.type == "builtin"
    assert bd.name == name
    assert bd.params == params


def test_unknown_builtin_distribution():
    """Ensure an error is raised if 'name' isn't in BUILTIN_DENSITY_MANIFEST."""
    with pytest.raises(ValueError, match="Unknown builtin distribution 'foobar'"):
        BuiltinDensity(type="builtin", name="foobar", params={"loc": 0, "scale": 1})


def test_invalid_param_key():
    """Ensure an error is raised if using a parameter key not allowed for 'norm'."""
    with pytest.raises(ValueError, match="Invalid parameter"):
        BuiltinDensity(type="builtin", name="norm", params={"loc": 0, "scale": 1, "alpha": 2.0})


def test_missing_required_param():
    """Ensure an error is raised if a required parameter is missing."""
    with pytest.raises(ValueError, match="Missing required parameter"):
        BuiltinDensity(type="builtin", name="norm", params={"loc": 0.0})


if __name__=='__main__':
    test_valid_builtin_distributions()
    test_unknown_builtin_distribution()
    test_invalid_param_key()
    test_missing_required_param()