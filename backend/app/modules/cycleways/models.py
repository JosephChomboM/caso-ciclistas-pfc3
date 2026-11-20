from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Cycleway(Base):
    __tablename__ = "cycleways"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    district: Mapped[str] = mapped_column(String(80), index=True)
    condition: Mapped[str] = mapped_column(String(40), default="Sin verificar")
    geometry: Mapped[list] = mapped_column(JSON)
    length_km: Mapped[float]
    source: Mapped[str] = mapped_column(String(200))
    is_demo: Mapped[bool] = mapped_column(default=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
