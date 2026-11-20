from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ParkingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    district: str
    latitude: float
    longitude: float
    address: str
    hours: str
    rack_type: str
    source: str
    is_demo: bool
    updated_at: datetime
