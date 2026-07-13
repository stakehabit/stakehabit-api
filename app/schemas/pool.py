from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class PoolBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration: int
    stake_amount: Decimal
    currency: str
    max_participants: int
    winner_split: int = Field(..., ge=0, le=100)
    charity: Optional[str] = None
    contract_address: Optional[str] = None
    creator_address: str


class PoolCreate(PoolBase):
    pass


class PoolParticipantBase(BaseModel):
    wallet_address: str
    signature: Optional[str] = None


class PoolParticipantRead(BaseModel):
    id: int
    wallet_address: str
    joined_at: datetime
    days_completed: int
    current_streak: int
    status: str

    model_config = {
        "from_attributes": True,
    }


class PoolCheckinCreate(BaseModel):
    wallet_address: str
    check_in_date: Optional[date] = None
    tx_hash: Optional[str] = None


class PoolCheckinRead(BaseModel):
    id: int
    participant_id: int
    pool_id: int
    check_in_date: date
    tx_hash: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class PoolRead(PoolBase):
    id: int
    status: str
    created_at: datetime
    participants: List[PoolParticipantRead] = []

    model_config = {
        "from_attributes": True,
    }


class StreakSummary(BaseModel):
    wallet_address: str
    current_streak: int
    longest_streak: int
    days_completed: int
