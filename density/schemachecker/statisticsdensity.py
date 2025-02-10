# density/schemachecker/statisticsdensity.py
from typing import Dict, Literal
from pydantic import Field, model_validator
from density.schemachecker.densitybase import DensityBase
from density.schemachecker.statisticsdensitymanifest import STATISTICS_DENSITY_LISTING


class StatisticsDensity(DensityBase):
    """
    A single distribution specification for a statistics distribution.

    Example:
      {
        "type": "statistics",
        "name": "normal",
        "params": { "mu": 0.0, "sigma": 1.0 }
      }
    """
    type: Literal["statistics"] = Field(default="statistics")
    name: str
    params: Dict[str, float] = Field(default_factory=dict)

    @model_validator(mode="after")
    def check_statistics_name_and_params(self):
        if self.name not in STATISTICS_DENSITY_LISTING:
            raise ValueError(
                f"Unknown statistics distribution '{self.name}'. "
                f"Allowed: {list(STATISTICS_DENSITY_LISTING.keys())}"
            )
        allowed_params = STATISTICS_DENSITY_LISTING[self.name]
        for k in self.params:
            if k not in allowed_params:
                raise ValueError(
                    f"Invalid parameter '{k}' for statistics distribution '{self.name}'. "
                    f"Allowed params: {allowed_params}"
                )
        return self
