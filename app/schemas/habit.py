from datetime import datetime

from pydantic import BaseModel


class HabitBase(BaseModel):
    title: str
    frequency: str
    target_days_per_week: int
    is_active: bool = True


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    title: str | None = None
    frequency: str | None = None
    target_days_per_week: int | None = None
    is_active: bool | None = None


class HabitRead(HabitBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
