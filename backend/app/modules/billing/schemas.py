from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class PlanChange(BaseModel):
    model_config = ConfigDict(extra="forbid")
    plan_code: Literal["free", "plus"]


class SubscriptionOut(BaseModel):
    plan_code: str
    mode: str = "demo"
    updated_at: datetime | None = None


class InvoiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    plan_code: str
    amount_centavos: int
    status: str
    created_at: datetime
    currency: str = "PEN"
