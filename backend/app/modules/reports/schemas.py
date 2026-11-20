from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ReportIn(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    cycleway_id: int = Field(gt=0)
    category: Literal["Obstáculo", "Vía deteriorada", "Incidente", "Señalización"]
    description: str = Field(min_length=10, max_length=1000)
    latitude: float = Field(ge=-12.5, le=-11.5, allow_inf_nan=False)
    longitude: float = Field(ge=-77.5, le=-76.5, allow_inf_nan=False)


class ReportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cycleway_id: int
    category: str
    description: str
    latitude: float
    longitude: float
    status: str
    created_at: datetime


class Decision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["published", "rejected"]
