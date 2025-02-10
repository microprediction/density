# density/schemachecker/mixture.py

from __future__ import annotations
from typing import List, Literal, TYPE_CHECKING, Annotated, Union
from pydantic import BaseModel, Field, field_validator

if TYPE_CHECKING:
    from density.schemachecker.scipydensity import ScipyDensity
    from density.schemachecker.builtindensity import BuiltinDensity
    from density.schemachecker.statisticsdensity import StatisticsDensity


#   We'll define a "MixtureComponent" referencing a union of ANY density, including MixtureSpec itself.
#   Because we want recursion, we can do a forward reference.

class MixtureComponent(BaseModel):
    density: Annotated[Union["ScipyDensity", "StatisticsDensity", "BuiltinDensity","MixtureSpec"], Field(discriminator="type")]
    weight: float


class MixtureSpec(BaseModel):
    """
    A mixture with type="mixture" and a list of components,
    each referencing any of the known density models.
    """
    type: Literal["mixture"] = Field(default="mixture")
    components: List[MixtureComponent]

    @field_validator("components")
    def check_sum_weights(cls, comps):
        total = sum(c.weight for c in comps)
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"Mixture weights must sum to 1.0 (got {total}).")
        return comps
