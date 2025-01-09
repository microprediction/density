import pytest
import math
import scipy.stats as st
from pydantic import ValidationError

from density.schemachecker.scipydensity import ScipyDensity, SCIPY_DENSITY_MANIFEST

def test_valid_scipy_norm():
    """Check that a standard 'norm' distribution is accepted."""
    sd = ScipyDensity(type="scipy", name="norm", params={"loc": 0, "scale": 1})
    assert sd.type == "scipy"
    assert sd.name == "norm"
    assert sd.params == {"loc": 0, "scale": 1}


def test_valid_scipy_expon():
    """Check that 'expon' distribution with valid keys is accepted."""
    sd = ScipyDensity(type="scipy", name="expon", params={"loc": 0, "scale": 2})
    assert sd.name == "expon"
    assert sd.params["scale"] == 2


@pytest.mark.parametrize("name,params", [
    ("t",         {"df": 3, "loc": 0, "scale": 1}),
    ("norm",      {"loc": 2, "scale": 0.5}),
    ("weibull_min", {"c": 1.5, "loc": 0, "scale": 2}),
    ("gamma",     {"a": 2.0, "loc": 0, "scale": 1.0}),
])
def test_valid_scipy_parametrized(name, params):
    """Check a variety of known distributions using parametrize."""
    sd = ScipyDensity(type="scipy", name=name, params=params)
    assert sd.name == name
    for k, v in params.items():
        assert sd.params[k] == v


def test_unknown_scipy_distribution():
    """Check that an invalid 'name' raises ValueError."""
    with pytest.raises(ValueError, match="Unknown scipy density 'unknown_dist'"):
        ScipyDensity(type="scipy", name="unknown_dist", params={"loc": 0, "scale": 1})


def test_invalid_param_key():
    """Check that an invalid param key raises ValueError."""
    with pytest.raises(ValueError, match="Invalid parameter 'foo'"):
        ScipyDensity(type="scipy", name="norm", params={"loc": 0, "scale": 1, "foo": 99})


@pytest.mark.parametrize("name,params,x,expected_pdf", [
    # Standard Normal PDF(0) = ~0.3989422804
    ("norm",       {"loc": 0, "scale": 1},  0.0, 0.3989422804),
    # Exponential with scale=2 => PDF(0) = 1/2
    ("expon",      {"loc": 0, "scale": 2},  0.0, 0.5),
    # Student's t with df=3, PDF(0) ~ 0.3675525969
    ("t",          {"df": 3, "loc": 0, "scale": 1}, 0.0, 0.3675525969),
    # Gamma(a=2, loc=0, scale=1) => PDF(2.0) ~ 0.2706705665
    ("gamma",      {"a": 2, "loc": 0, "scale": 1}, 2.0, 0.2706705665),
    # Weibull_min(c=1.5, loc=0, scale=2), PDF(0) => 0.0 if c>1, let's pick x=1 maybe
    # PDF(1) ~ ?
    ("weibull_min", {"c": 1.5, "loc": 0, "scale": 2}, 1.0, 0.372391688219)
])
def test_integration_scipy_pdf(name, params, x, expected_pdf):
    """
    Integration test: instantiate the distribution with scipy.stats
    and evaluate the PDF at a specified point x. Compare to expected.
    """
    # 1) Validate with Pydantic
    sd = ScipyDensity(type="scipy", name=name, params=params)

    # 2) Instantiate the actual scipy.stats distribution
    dist_class = getattr(st, name)  # e.g. st.norm, st.gamma, st.t, etc.
    dist = dist_class(**params)

    # 3) Evaluate PDF
    got_pdf = dist.pdf(x)
    # 4) Compare to expected
    assert math.isclose(got_pdf, expected_pdf, rel_tol=1e-7), \
        f"PDF mismatch for {name} at x={x}: got {got_pdf}, expected {expected_pdf}"
