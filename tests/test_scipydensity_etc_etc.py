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
    ("t", {"df": 3, "loc": 0, "scale": 1}),
    ("norm", {"loc": 2, "scale": 0.5}),
    ("weibull_min", {"c": 1.5, "loc": 0, "scale": 2}),
    ("gamma", {"a": 2.0, "loc": 0, "scale": 1.0}),
    ("weibull_max", {"c": 1.5, "loc": 0, "scale": 2}),
    ("beta", {"a": 2.0, "b": 5.0, "loc": 0, "scale": 1.0}),
    ("lognorm", {"s": 1.0, "loc": 0, "scale": 2.0}),
    ("chi", {"df": 2, "loc": 0, "scale": 1.0}),
    ("chi2", {"df": 4, "loc": 0, "scale": 1.0}),
    ("rayleigh", {"loc": 0, "scale": 2.0}),
    ("pareto", {"b": 2.0, "loc": 0, "scale": 1.0}),
    ("cauchy", {"loc": 0, "scale": 1.0}),
    ("laplace", {"loc": 0, "scale": 1.0}),
    ("f", {"dfn": 2, "dfd": 5, "loc": 0, "scale": 1.0}),
])
def test_valid_scipy_more_distributions(name, params):
    """
    Check that a variety of extended distributions
    are accepted by ScipyDensity if we have them in SCIPY_DENSITY_MANIFEST.
    """
    sd = ScipyDensity(type="scipy", name=name, params=params)
    assert sd.name == name
    # Confirm the params match
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
    # Already-verified ones
    ("cauchy",    {"loc": 0, "scale": 1},  0.0, 0.3183098861837907),   # ~1/π
    # lognorm(s=1, loc=0, scale=1).pdf(1.0) => ~0.3989422804014327
    ("lognorm",   {"s": 1.0, "loc": 0, "scale": 1.0}, 1.0, 0.3989422804),
    # f(dfn=2, dfd=5).pdf(1.0) => ~0.308000821694...
    # We'll store 0.3080 (or 0.308001) with a small tolerance
    ("f",         {"dfn": 2, "dfd": 5, "loc": 0, "scale": 1.0}, 1.0, 0.3080008217),
    # Let's add a few more examples for demonstration:
    # beta(a=2, b=5).pdf(0.3) => ~ 1.265625
    ("beta",      {"a": 2, "b": 5, "loc": 0, "scale": 1}, 0.3, 2.16089999999999),
    # chi2(df=4).pdf(2) => ~0.1465251111
    ("chi2",      {"df": 4, "loc": 0, "scale": 1}, 2.0, 0.183939720585721),
    # rayleigh(loc=0, scale=2).pdf(1) => ~0.2206242256
    ("rayleigh",  {"loc": 0, "scale": 2}, 1.0, 0.2206242256),
])





def test_integration_scipy_pdf(name, params, x, expected_pdf):
    """
    Integration test: instantiate the distribution with scipy.stats
    and evaluate the PDF at a specified point x. Compare to expected.
    (We've only added a few "new" ones here for demonstration.)
    """
    # 1) Validate with Pydantic
    sd = ScipyDensity(type="scipy", name=name, params=params)

    # 2) Instantiate the actual scipy.stats distribution
    dist_class = getattr(st, name)  # e.g. st.norm, st.gamma, st.t, etc.
    dist = dist_class(**params)

    # 3) Evaluate PDF
    got_pdf = dist.pdf(x)
    # 4) Compare to expected
    assert math.isclose(got_pdf, expected_pdf, rel_tol=1e-5), \
        f"PDF mismatch for {name} at x={x}: got {got_pdf}, expected {expected_pdf}"
