from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class PoolBase(BaseModel):
    title: str
    description: str | None = None
    duration: int
    stake_amount: Decimal
    currency: str
    max_participants: int
    winner_split: int = Field(..., ge=0, le=100)
    charity: str | None = None
    contract_address: str | None = None
    creator_address: str


class PoolCreate(PoolBase):
    pass


class PoolParticipantBase(BaseModel):
    wallet_address: str
    signature: str | None = None


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
    check_in_date: date | None = None
    tx_hash: str | None = None


class PoolCheckinRead(BaseModel):
    id: int
    participant_id: int
    pool_id: int
    check_in_date: date
    tx_hash: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class PoolRead(PoolBase):
    id: int
    status: str
    created_at: datetime
    participants: list[PoolParticipantRead] = []

    model_config = {
        "from_attributes": True,
    }


class StreakSummary(BaseModel):
    wallet_address: str
    current_streak: int
    longest_streak: int
    days_completed: int
