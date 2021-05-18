from pydantic import Field, validator
from typing import Optional
import qcelemental
from mmelemental.models.base import ProtoModel

__all__ = ["Harmonic"]


class Harmonic(ProtoModel):
    """
    Linear spring bond model: Energy = 1/2 * spring * (distance - length)**2. "
    """

    spring: qcelemental.models.types.Array[float] = Field(
        ..., description="Bond spring constant. Default unit is kJ/(mol*angstrom**2)."
    )
    spring_units: Optional[str] = Field(
        "kJ/(mol*angstrom**2)", description="Bond spring constant unit."
    )

    @validator("spring", allow_reuse=True)
    def _valid_length(cls, v):
        assert len(v.shape) == 1, "Bond spring constants must be a 1D array!"
        return v