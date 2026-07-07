from __future__ import annotations

from typing import Optional
from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitUpdate


def get_habits_for_user(db: Session, user_id: int) -> list[Habit]:
    return db.query(Habit).filter(Habit.user_id == user_id).all()


def get_habit_by_id(db: Session, habit_id: int, user_id: int) -> Optional[Habit]:
    return db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user_id).first()


def create_habit(db: Session, user_id: int, habit_create: HabitCreate) -> Habit:
    habit = Habit(user_id=user_id, **habit_create.model_dump())
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


def update_habit(db: Session, habit: Habit, habit_update: HabitUpdate) -> Habit:
    update_data = habit_update.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(habit, key, value)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


def delete_habit(db: Session, habit: Habit) -> None:
    db.delete(habit)
    db.commit()
