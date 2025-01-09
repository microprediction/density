# density/schemachecker/mixture.py
# tests/test_mixture.py
import pytest
from pydantic import ValidationError

# Import the model you want to test
from density.schemachecker.mixturespec import MixtureSpec
from density.schemachecker.scipydensity import ScipyDensity
from density.schemachecker.builtindensity import BuiltinDensity

def test_valid_mixture_scipy_builtin():
    """A valid mixture of one scipy distribution and one builtin distribution."""
    mixture_data = {
        "type": "mixture",
        "components": [
            {
                "density": {
                    "type": "scipy",
                    "name": "norm",
                    "params": {"loc": 0, "scale": 1}
                },
                "weight": 0.6
            },
            {
                "density": {
                    "type": "builtin",
                    "name": "normal",
                    "params": {"mu": 0, "sigma": 1}
                },
                "weight": 0.4
            }
        ]
    }
    mixture = MixtureSpec(**mixture_data)
    assert mixture.type == "mixture"
    assert len(mixture.components) == 2
    # Check the sum of weights is indeed 1.0
    total_weight = sum(comp.weight for comp in mixture.components)
    assert abs(total_weight - 1.0) < 1e-9

def test_invalid_sum_of_weights():
    """Ensure an error is raised if mixture weights don't sum to 1."""
    bad_mixture_data = {
        "type": "mixture",
        "components": [
            {
                "density": {
                    "type": "scipy",
                    "name": "norm",
                    "params": {"loc": 0, "scale": 1}
                },
                "weight": 0.3
            },
            {
                "density": {
                    "type": "builtin",
                    "name": "normal",
                    "params": {"mu": 0, "sigma": 1}
                },
                "weight": 0.3
            }
        ]
    }
    with pytest.raises(ValidationError, match="Mixture weights must sum to 1.0"):
        MixtureSpec(**bad_mixture_data)

def test_mixture_with_unknown_distribution():
    """If a component references an unknown distribution, it should fail."""
    bad_mixture_data = {
        "type": "mixture",
        "components": [
            {
                "density": {
                    "type": "scipy",
                    "name": "norm",
                    "params": {"loc": 0, "scale": 1}
                },
                "weight": 0.5
            },
            {
                "density": {
                    "type": "builtin",
                    "name": "foobar",  # invalid builtin name
                    "params": {"mu": 0, "sigma": 1}
                },
                "weight": 0.5
            }
        ]
    }
    # Expecting an error about "Unknown builtin distribution 'foobar'"
    with pytest.raises(ValidationError, match="Unknown builtin distribution 'foobar'"):
        MixtureSpec(**bad_mixture_data)

def test_nested_mixture_ok():
    """Example of a nested mixture, if your schema allows it."""
    nested_data = {
        "type": "mixture",
        "components": [
            {
                "density": {
                    "type": "mixture",  # Another mixture inside
                    "components": [
                        {
                            "density": {
                                "type": "scipy",
                                "name": "expon",
                                "params": {"loc": 0, "scale": 2}
                            },
                            "weight": 0.5
                        },
                        {
                            "density": {
                                "type": "builtin",
                                "name": "normal",
                                "params": {"mu": 0, "sigma": 1}
                            },
                            "weight": 0.5
                        }
                    ]
                },
                "weight": 0.4
            },
            {
                "density": {
                    "type": "scipy",
                    "name": "t",
                    "params": {"df": 3, "loc": 0, "scale": 1}
                },
                "weight": 0.6
            }
        ]
    }
    mixture = MixtureSpec(**nested_data)
    assert len(mixture.components) == 2
    # The first component is another mixture with 2 sub-components
    nested_mix = mixture.components[0].density
    assert nested_mix.type == "mixture"
    assert len(nested_mix.components) == 2

def test_nested_mixture_invalid_sum():
    """Nested mixture where the nested mixture's weights don't sum to 1 -> error."""
    bad_nested_data = {
        "type": "mixture",
        "components": [
            {
                "density": {
                    "type": "mixture",
                    "components": [
                        {
                            "density": {
                                "type": "builtin",
                                "name": "normal",
                                "params": {"mu": 1, "sigma": 2}
                            },
                            "weight": 0.3
                        },
                        {
                            "density": {
                                "type": "builtin",
                                "name": "normal",
                                "params": {"mu": 0, "sigma": 1}
                            },
                            "weight": 0.3
                        }
                    ]
                },
                "weight": 0.4
            },
            {
                "density": {
                    "type": "scipy",
                    "name": "norm",
                    "params": {"loc": 2, "scale": 0.5}
                },
                "weight": 0.6
            }
        ]
    }
    # The nested mixture's sum is 0.6, not 1.0 => expect an error
    with pytest.raises(ValidationError, match="Mixture weights must sum to 1.0"):
        MixtureSpec(**bad_nested_data)
