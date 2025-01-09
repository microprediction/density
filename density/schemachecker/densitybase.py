# density/schemachecker/densitybase.py

from pydantic import BaseModel


class DensityBase(BaseModel):
    """
    Optional common base if you want
    any shared logic or methods across distributions.
    """
    pass
