from __future__ import annotations

from datetime import date, timedelta
from typing import Optional

from app.models.checkin import Checkin


class StreakResult:
    def __init__(self, current_streak: int, longest_streak: int, total_completed_checkins: int) -> None:
        self.current_streak = current_streak
        self.longest_streak = longest_streak
        self.total_completed_checkins = total_completed_checkins


def calculate_streaks(checkins: list[Checkin], today: Optional[date] = None) -> StreakResult:
    dates = sorted({checkin.date for checkin in checkins})
    today = today or date.today()
    current_streak = 0
    longest_streak = 0
    streak = 0
    previous_date: Optional[date] = None

    for checkin_date in dates:
        if previous_date is None or checkin_date != previous_date + timedelta(days=1):
            streak = 1
        else:
            streak += 1
        longest_streak = max(longest_streak, streak)
        previous_date = checkin_date

    if dates:
        backward_date = today
        while backward_date in dates:
            current_streak += 1
            backward_date -= timedelta(days=1)

    return StreakResult(
        current_streak=current_streak,
        longest_streak=longest_streak,
        total_completed_checkins=len(dates),
    )
