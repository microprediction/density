# density/schemachecker/builtindensity.py
from typing import Dict, Literal
from pydantic import Field, model_validator
from density.schemachecker.densitybase import DensityBase

ALLOWED_BUILTIN_DISTS = {
    # We only allow "normal"
    "normal": {"mu", "sigma"}  # For statistics.NormalDist
}


class BuiltinDensity(DensityBase):
    """
    A single distribution specification for a "builtin" or "pure Python" distribution.
    Currently we only allow 'name="normal"' referencing `statistics.NormalDist`.

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
        if self.name not in ALLOWED_BUILTIN_DISTS:
            raise ValueError(
                f"Unknown builtin distribution '{self.name}'. "
                f"Allowed: {list(ALLOWED_BUILTIN_DISTS.keys())}"
            )
        allowed_params = ALLOWED_BUILTIN_DISTS[self.name]
        for k in self.params:
            if k not in allowed_params:
                raise ValueError(
                    f"Invalid parameter '{k}' for builtin distribution '{self.name}'. "
                    f"Allowed params: {allowed_params}"
                )
        return self
