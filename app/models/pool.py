from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Pool(Base):
    __tablename__ = "pools"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    duration = Column(Integer, nullable=False)
    stake_amount = Column(Numeric(20, 7), nullable=False)
    currency = Column(String(10), nullable=False)
    max_participants = Column(Integer, nullable=False)
    winner_split = Column(Integer, nullable=False)
    charity = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    contract_address = Column(String(56), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    creator_address = Column(String(56), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    creator = relationship("User")
    participants = relationship("PoolParticipant", back_populates="pool", cascade="all, delete-orphan")
    checkins = relationship("PoolCheckin", back_populates="pool", cascade="all, delete-orphan")
