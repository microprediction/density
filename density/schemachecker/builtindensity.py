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
        "name": "norm",
        "params": { "loc": 0.0, "scale": 1.0 }
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
        allowed_params = BUILTIN_DENSITY_MANIFEST[self.name]
        for param_key in self.params:
            if param_key not in allowed_params:
                raise ValueError(
                    f"Invalid parameter '{param_key}' for builtin distribution '{self.name}'. "
                    f"Allowed params: {allowed_params}"
                )

        # Check for missing required parameters
        missing_params = allowed_params - self.params.keys()
        if missing_params:
            raise ValueError(
                f"Missing required parameter(s) {missing_params} for builtin distribution '{self.name}'"
            )

        return self
