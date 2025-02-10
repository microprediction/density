# density/schemachecker/builtindensity.py
from typing import Dict, Literal
from pydantic import Field, model_validator
from density.schemachecker.densitybase import DensityBase
from density.schemachecker.builtindensitymanifest import BUILTIN_DENSITY_MANIFEST


class BuiltinDensity(DensityBase):
    """
    A single distribution specification for a "builtin" or "pure Python" distribution.


    Example:
      {
        "type": "builtin",
        "name": "normal",
        "params": { "mu": 0.0, "sigma": 1.0 }
      }
    """
    type: Literal["builtin"] = Field(default="builtin")
    name: str
    params: Dict[str, float] = Field(default_factory=dict)

    @model_validator(mode="after")
    def check_builtin_name_and_params(self):
        if self.name not in BUILTIN_DENSITY_MANIFEST:
            raise ValueError(
                f"Unknown builtin distribution '{self.name}'. "
                f"Allowed: {list(BUILTIN_DENSITY_MANIFEST.keys())}"
            )
        allowed_params = [self.name]
        for k in self.params:
            if k not in allowed_params:
                raise ValueError(
                    f"Invalid parameter '{k}' for builtin distribution '{self.name}'. "
                    f"Allowed params: {allowed_params}"
                )
        return self
