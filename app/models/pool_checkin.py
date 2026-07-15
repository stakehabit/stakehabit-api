from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class PoolCheckin(Base):
    __tablename__ = "pool_checkins"
    __table_args__ = (UniqueConstraint("participant_id", "check_in_date", name="uq_participant_checkin"),)

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, ForeignKey("pool_participants.id", ondelete="CASCADE"), nullable=False)
    pool_id = Column(Integer, ForeignKey("pools.id", ondelete="CASCADE"), nullable=False)
    check_in_date = Column(Date, nullable=False)
    tx_hash = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    participant = relationship("PoolParticipant", back_populates="checkins")
    pool = relationship("Pool", back_populates="checkins")
