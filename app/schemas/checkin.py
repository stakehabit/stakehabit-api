from datetime import date as date_type, datetime
from typing import Optional

from pydantic import BaseModel


class CheckinCreate(BaseModel):
    date: Optional[date_type] = None


class CheckinRead(BaseModel):
    id: int
    habit_id: int
    date: date_type
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
