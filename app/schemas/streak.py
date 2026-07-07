from pydantic import BaseModel


class StreakRead(BaseModel):
    current_streak: int
    longest_streak: int
    total_completed_checkins: int
