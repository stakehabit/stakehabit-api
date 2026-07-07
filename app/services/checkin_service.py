from __future__ import annotations

from datetime import date
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.checkin import Checkin
from app.models.habit import Habit
from app.schemas.checkin import CheckinCreate


class DuplicateCheckinError(ValueError):
    pass


def create_checkin(db: Session, habit: Habit, checkin_create: CheckinCreate) -> Checkin:
    checkin_date = checkin_create.date or date.today()
    checkin = Checkin(habit_id=habit.id, date=checkin_date)
    db.add(checkin)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        if "uq_habit_date" in str(error.orig):
            raise DuplicateCheckinError("A check-in already exists for this habit on that date.") from error
        raise
    db.refresh(checkin)
    return checkin


def get_checkins_by_habit(db: Session, habit_id: int) -> list[Checkin]:
    return db.query(Checkin).filter(Checkin.habit_id == habit_id).order_by(Checkin.date.asc()).all()
