from datetime import date as date_type
from datetime import datetime

from pydantic import BaseModel


class CheckinCreate(BaseModel):
    date: date_type | None = None


class CheckinRead(BaseModel):
    id: int
    habit_id: int
    date: date_type
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
