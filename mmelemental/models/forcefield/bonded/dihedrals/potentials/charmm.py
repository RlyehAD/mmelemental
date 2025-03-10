from pydantic import Field, validator, root_validator
from typing import Optional
from cmselemental.types import Array
from mmelemental.models.base import ProtoModel

__all__ = ["Charmm"]


class Charmm(ProtoModel):
    """
    Charmm-style dihedral potential: Energy = energy * (1 + cos(periodicity * angle - phase)).
    """

    energy: Array[float] = Field(
        ...,
        description="Dihedral energy constant. Default unit is kJ/mol.",
    )
    energy_units: Optional[str] = Field(
        "kJ/mol", description="Dihedral energy constant unit."
    )
    periodicity: Array[int] = Field(
        ...,
        description="Dihedral periodicity factor, must be >= 0.",
    )
    phase: Array[float] = Field(
        ...,
        description="Dihedral phase angle. Default unit is degrees.",
    )
    phase_units: Optional[str] = Field(
        "degrees", description="Dihedral phase angle unit."
    )

    @validator("energy", allow_reuse=True)
    def _valid_shape(cls, v):
        assert len(v.shape) == 1, "Dihedral energy constant must be a 1D array!"
        return v

    @validator("periodicity", allow_reuse=True)
    def _valid_periodicity(cls, v):
        assert (v >= 0).all(), "Dihedral periodicity must be >= 0."
        return v

    @root_validator(allow_reuse=True)
    def _valid_arrays(cls, values):
        energy_shape = values["energy"].shape
        periodicity_shape = values["periodicity"].shape
        phase_shape = values["phase"].shape
        assert (
            energy_shape == periodicity_shape == phase_shape
        ), f"Energy ({energy_shape}), periodocity ({periodicity_shape}), and phase ({phase_shape}) must have the same shape."
        return values
