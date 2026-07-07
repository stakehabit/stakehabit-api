from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class CheckinCreate(BaseModel):
    date: Optional[date] = None


class CheckinRead(BaseModel):
    id: int
    habit_id: int
    date: date
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
