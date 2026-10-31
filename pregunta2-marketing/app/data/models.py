from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.data.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"
    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(String(120))
    product: Mapped[str] = mapped_column(String(120))
    audience: Mapped[str] = mapped_column(String(180))
    objective: Mapped[str] = mapped_column(String(180))
    original_path: Mapped[str] = mapped_column(String(255))
    scripts: Mapped[str] = mapped_column(Text)
    selected_script: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="GUIONES")
    social_id: Mapped[str | None] = mapped_column(String(180), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    assets: Mapped[list["Asset"]] = relationship(back_populates="campaign", cascade="all, delete-orphan")


class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[int] = mapped_column(primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(String(20))
    path: Mapped[str] = mapped_column(String(255))
    campaign: Mapped[Campaign] = relationship(back_populates="assets")

