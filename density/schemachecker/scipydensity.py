from typing import Dict, Literal
from pydantic import Field, model_validator
from .densitybase import DensityBase

VALID_SCIPY_DENSITIES = {
    "norm":         {"loc", "scale"},
    "expon":        {"loc", "scale"},
    "t":            {"df", "loc", "scale"},
    "weibull_min":  {"c", "loc", "scale"},
    "gamma":        {"a", "loc", "scale"},
    "weibull_max": {"c", "loc", "scale"},
    "beta": {"a", "b", "loc", "scale"},
    "lognorm": {"s", "loc", "scale"},
    "chi": {"df", "loc", "scale"},
    "chi2": {"df", "loc", "scale"},
    "rayleigh": {"loc", "scale"},
    "pareto": {"b", "loc", "scale"},
    "cauchy": {"loc", "scale"},
    "laplace": {"loc", "scale"},
    "f": {"dfn", "dfd", "loc", "scale"},
}


class ScipyDensity(DensityBase):
    """
    Example:
      {
        "type": "scipy",
        "name": "norm",
        "params": {"loc": 0, "scale": 1}
      }
    """
    type: Literal["scipy"] = Field(default="scipy")
    name: str
    params: Dict[str, float] = Field(default_factory=dict)

    @model_validator(mode="after")
    def check_scipy_name_and_params(self):
        """
        Called after Pydantic has constructed 'self' (i.e., the model instance).
        We can now check that self.name is in the known dictionary, etc.
        """
        if self.name not in VALID_SCIPY_DENSITIES:
            raise ValueError(
                f"Unknown scipy density '{self.name}'. Allowed: {list(VALID_SCIPY_DENSITIES.keys())}"
            )
        allowed_keys = VALID_SCIPY_DENSITIES[self.name]
        for param_key in self.params.keys():
            if param_key not in allowed_keys:
                raise ValueError(
                    f"Invalid parameter '{param_key}' for '{self.name}'. "
                    f"Allowed params: {allowed_keys}"
                )
        return self
