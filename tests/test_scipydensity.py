# tests/test_scipydensity.py

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
])
def test_valid_scipy_parametrized(name, params):
    """Check a couple of known distributions using parametrize."""
    sd = ScipyDensity(type="scipy", name=name, params=params)
    assert sd.name == name
    assert sd.params == params


def test_unknown_scipy_distribution():
    """Check that an invalid 'name' raises ValueError."""
    with pytest.raises(ValueError, match="Unknown scipy density 'unknown_dist'"):
        ScipyDensity(type="scipy", name="unknown_dist", params={"loc": 0, "scale": 1})


def test_invalid_param_key():
    """Check that an invalid param key raises ValueError."""
    with pytest.raises(ValueError, match="Invalid parameter 'foo'"):
        ScipyDensity(type="scipy", name="norm", params={"loc": 0, "scale": 1, "foo": 99})


def test_integration_scipy_pdf():
    """
    Example showing how to instantiate a real scipy distribution
    from the validated params and evaluate a PDF.
    """
    # 1) Validate the schema
    sd = ScipyDensity(type="scipy", name="norm", params={"loc": 0, "scale": 1})

    # 2) Instantiate the actual scipy.stats distribution
    dist_class = getattr(st, sd.name)  # e.g. st.norm
    dist = dist_class(**sd.params)  # st.norm(loc=0, scale=1)

    # 3) Evaluate PDF at x=0
    pdf_val = dist.pdf(0.0)
    # For a standard normal, pdf(0) ~= 0.39894228
    assert math.isclose(pdf_val, 0.3989422804, rel_tol=1e-7)


def test_integration_scipy_pdf_expon():
    """
    Another integration test with 'expon' distribution.
    """
    sd = ScipyDensity(type="scipy", name="expon", params={"loc": 0, "scale": 2})
    dist_class = getattr(st, sd.name)  # st.expon
    dist = dist_class(**sd.params)
    # Exponential PDF at x=0, with scale=2 => 1/2
    pdf_val = dist.pdf(0.0)
    assert math.isclose(pdf_val, 0.5, rel_tol=1e-7)
