from typing import Dict, Literal
from pydantic import Field, model_validator
from .densitybase import DensityBase
from density.schemachecker.scipydensitymanifest import SCIPY_DENSITY_MANIFEST


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
        if self.name not in SCIPY_DENSITY_MANIFEST:
            raise ValueError(
                f"Unknown scipy density '{self.name}'. Allowed: {list(SCIPY_DENSITY_MANIFEST.keys())}"
            )
        allowed_keys = SCIPY_DENSITY_MANIFEST[self.name]
        for param_key in self.params.keys():
            if param_key not in allowed_keys:
                raise ValueError(
                    f"Invalid parameter '{param_key}' for '{self.name}'. "
                    f"Allowed params: {allowed_keys}"
                )
        return self
