from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HabitBase(BaseModel):
    title: str
    frequency: str
    target_days_per_week: int
    is_active: bool = True


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    title: Optional[str] = None
    frequency: Optional[str] = None
    target_days_per_week: Optional[int] = None
    is_active: Optional[bool] = None


class HabitRead(HabitBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
