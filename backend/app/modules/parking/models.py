from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Parking(Base):
    __tablename__ = "parking"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    district: Mapped[str] = mapped_column(String(80), index=True)
    latitude: Mapped[float]
    longitude: Mapped[float]
    address: Mapped[str] = mapped_column(String(200))
    hours: Mapped[str] = mapped_column(String(120), default="No informado")
    rack_type: Mapped[str] = mapped_column(String(120), default="No informado")
    source: Mapped[str] = mapped_column(String(200))
    is_demo: Mapped[bool] = mapped_column(default=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "parking_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    parking_id: Mapped[int] = mapped_column(ForeignKey("parking.id", ondelete="CASCADE"))
