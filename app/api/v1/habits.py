from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.schemas.checkin import CheckinCreate, CheckinRead
from app.schemas.habit import HabitCreate, HabitRead, HabitUpdate
from app.schemas.streak import StreakRead
from app.services.checkin_service import DuplicateCheckinError, create_checkin, get_checkins_by_habit
from app.services.habit_service import (
    create_habit,
    delete_habit,
    get_habit_by_id,
    get_habits_for_user,
    update_habit,
)
from app.services.streak_service import calculate_streaks

router = APIRouter()


@router.get("/habits", response_model=list[HabitRead])
def list_habits(current_user=Depends(get_current_user), db: Session = Depends(get_db)) -> list[HabitRead]:
    return get_habits_for_user(db, user_id=current_user.id)


@router.post("/habits", response_model=HabitRead, status_code=status.HTTP_201_CREATED)
def create_new_habit(
    habit_create: HabitCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)
) -> HabitRead:
    return create_habit(db, user_id=current_user.id, habit_create=habit_create)


@router.get("/habits/{habit_id}", response_model=HabitRead)
def get_habit(habit_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)) -> HabitRead:
    habit = get_habit_by_id(db, habit_id=habit_id, user_id=current_user.id)
    if habit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    return habit


@router.patch("/habits/{habit_id}", response_model=HabitRead)
def patch_habit(
    habit_id: int, habit_update: HabitUpdate, current_user=Depends(get_current_user), db: Session = Depends(get_db)
) -> HabitRead:
    habit = get_habit_by_id(db, habit_id=habit_id, user_id=current_user.id)
    if habit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    return update_habit(db, habit=habit, habit_update=habit_update)


@router.delete("/habits/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_habit(habit_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    habit = get_habit_by_id(db, habit_id=habit_id, user_id=current_user.id)
    if habit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    delete_habit(db, habit=habit)


@router.post("/habits/{habit_id}/checkins", response_model=CheckinRead, status_code=status.HTTP_201_CREATED)
def add_checkin(
    habit_id: int, checkin_create: CheckinCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)
) -> CheckinRead:
    habit = get_habit_by_id(db, habit_id=habit_id, user_id=current_user.id)
    if habit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    try:
        return create_checkin(db, habit=habit, checkin_create=checkin_create)
    except DuplicateCheckinError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.get("/habits/{habit_id}/streak", response_model=StreakRead)
def get_streak(habit_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)) -> StreakRead:
    habit = get_habit_by_id(db, habit_id=habit_id, user_id=current_user.id)
    if habit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    checkins = get_checkins_by_habit(db, habit_id=habit.id)
    streak = calculate_streaks(checkins)
    return StreakRead(
        current_streak=streak.current_streak,
        longest_streak=streak.longest_streak,
        total_completed_checkins=streak.total_completed_checkins,
    )
