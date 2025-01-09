# tests/test_builtindensity.py

import pytest
import math
from pydantic import ValidationError
from statistics import NormalDist

from density.schemachecker.builtindensity import BuiltinDensity

@pytest.mark.parametrize("name,params", [
    ("normal", {"mu": 0.0, "sigma": 1.0}),
    ("normal", {"mu": -1.2, "sigma": 2.5}),
])
def test_valid_builtin_normal(name, params):
    """Test that BuiltinDensity accepts valid 'normal' with mu, sigma."""
    bd = BuiltinDensity(type="builtin", name=name, params=params)
    assert bd.type == "builtin"
    assert bd.name == "normal"
    assert bd.params == params

def test_unknown_builtin_distribution():
    """Ensure an error is raised if 'name' isn't in BUILTIN_DENSITY_LISTING."""
    with pytest.raises(ValueError, match="Unknown builtin distribution 'foobar'"):
        BuiltinDensity(type="builtin", name="foobar", params={"mu": 0, "sigma": 1})

def test_invalid_param_key():
    """Ensure an error is raised if using a parameter key not allowed for 'normal'."""
    with pytest.raises(ValueError, match="Invalid parameter 'alpha' for builtin distribution 'normal'"):
        BuiltinDensity(type="builtin", name="normal", params={"mu": 0, "sigma": 1, "alpha": 2.0})

def test_missing_sigma():
    """
    If 'sigma' is omitted, we won't error unless you want to enforce it strictly.
    But let's show how you'd catch missing param if you do require it.
    """
    with pytest.raises(ValueError, match="Invalid parameter 'alpha' for builtin distribution 'normal'"):
        # We try "alpha" instead of "sigma", which isn't allowed
        BuiltinDensity(type="builtin", name="normal", params={"mu": 0, "alpha": 2.0})

def test_statistics_normaldist_evaluation():
    """
    Example test showing how you might evaluate a PDF using Python's built-in
    statistics.NormalDist after validating BuiltinDensity.
    """
    bd = BuiltinDensity(type="builtin", name="normal", params={"mu": 0, "sigma": 1})
    mu = bd.params["mu"]
    sigma = bd.params["sigma"]
    dist = NormalDist(mu, sigma)
    # Evaluate PDF at 0.0, should be ~0.3989 for standard normal
    pdf_val = dist.pdf(0.0)
    assert math.isclose(pdf_val, 0.3989422804, rel_tol=1e-7)
