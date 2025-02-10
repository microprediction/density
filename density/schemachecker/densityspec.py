from density.schemachecker.scipydensity import ScipyDensity
from density.schemachecker.builtindensity import BuiltinDensity
from density.schemachecker.statisticsdensity import StatisticsDensity
from density.schemachecker.mixturespec import MixtureSpec
from typing import Union, Annotated
from pydantic import Field, RootModel

# A union of the three models, discriminated by `type`.
AnyDensityUnion = Union[ScipyDensity, BuiltinDensity, StatisticsDensity, MixtureSpec]
DiscriminatedAnyDensity = Annotated[AnyDensityUnion, Field(discriminator="type")]


class DensitySpec(RootModel[DiscriminatedAnyDensity]):
    """
    The top-level model that can parse EITHER a single density
    or a mixture, discriminated by 'type'.
    Uses Pydantic 2's RootModel, not BaseModel + __root__.
    """
    pass


DensitySpec.model_rebuild()
