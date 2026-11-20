from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CyclewayOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    district: str
    condition: str
    geometry: list[list[float]]
    length_km: float
    source: str
    is_demo: bool
    updated_at: datetime
