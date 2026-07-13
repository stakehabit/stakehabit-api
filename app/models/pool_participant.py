from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class PoolParticipant(Base):
    __tablename__ = "pool_participants"
    __table_args__ = (UniqueConstraint("pool_id", "wallet_address", name="uq_pool_wallet"),)

    id = Column(Integer, primary_key=True, index=True)
    pool_id = Column(Integer, ForeignKey("pools.id", ondelete="CASCADE"), nullable=False)
    wallet_address = Column(String(56), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    days_completed = Column(Integer, default=0, nullable=False)
    current_streak = Column(Integer, default=0, nullable=False)
    status = Column(String(20), nullable=False, default="active")

    pool = relationship("Pool", back_populates="participants")
    checkins = relationship("PoolCheckin", back_populates="participant", cascade="all, delete-orphan")
