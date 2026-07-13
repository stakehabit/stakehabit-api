from datetime import date, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.pool import Pool
from app.models.pool_checkin import PoolCheckin
from app.models.pool_participant import PoolParticipant
from app.schemas.pool import PoolCreate, PoolParticipantBase, PoolCheckinCreate


class PoolJoinError(ValueError):
    pass


class PoolCheckinError(ValueError):
    pass


def get_pools(db: Session) -> list[Pool]:
    return db.query(Pool).filter(Pool.status == "active").all()


def get_pool_by_id(db: Session, pool_id: int) -> Pool | None:
    return db.query(Pool).filter(Pool.id == pool_id).first()


def create_pool(db: Session, pool_create: PoolCreate, creator_id: int | None = None) -> Pool:
    pool = Pool(**pool_create.model_dump(), creator_id=creator_id)
    db.add(pool)
    db.commit()
    db.refresh(pool)
    return pool


def get_participant(db: Session, pool_id: int, wallet_address: str) -> PoolParticipant | None:
    return db.query(PoolParticipant).filter(
        PoolParticipant.pool_id == pool_id,
        PoolParticipant.wallet_address == wallet_address,
    ).first()


def join_pool(db: Session, pool: Pool, participant_data: PoolParticipantBase) -> PoolParticipant:
    if pool.status != "active":
        raise PoolJoinError("Cannot join a pool that is not active.")

    if pool.max_participants <= len(pool.participants):
        raise PoolJoinError("Pool has reached maximum participants.")

    participant = PoolParticipant(pool_id=pool.id, wallet_address=participant_data.wallet_address)
    db.add(participant)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        error_text = str(error.orig).lower()
        if "uq_pool_wallet" in error_text or "pool_participants.pool_id, pool_participants.wallet_address" in error_text:
            raise PoolJoinError("Wallet already joined this pool.") from error
        raise
    db.refresh(participant)
    return participant


def get_pool_participants(db: Session, pool_id: int) -> list[PoolParticipant]:
    return db.query(PoolParticipant).filter(PoolParticipant.pool_id == pool_id).order_by(
        PoolParticipant.current_streak.desc(), PoolParticipant.days_completed.desc(), PoolParticipant.joined_at.asc()
    ).all()


def get_checkins_for_wallet(db: Session, pool_id: int, wallet_address: str) -> list[PoolCheckin]:
    participant = get_participant(db, pool_id=pool_id, wallet_address=wallet_address)
    if not participant:
        return []
    return db.query(PoolCheckin).filter(
        PoolCheckin.pool_id == pool_id,
        PoolCheckin.participant_id == participant.id,
    ).order_by(PoolCheckin.check_in_date.asc()).all()


def _calculate_current_streak(dates: list[date], today: date) -> int:
    dates_set = set(dates)
    streak = 0
    current_date = today
    while current_date in dates_set:
        streak += 1
        current_date -= timedelta(days=1)
    return streak


def submit_checkin(db: Session, pool: Pool, checkin_data: PoolCheckinCreate) -> PoolCheckin:
    participant = get_participant(db, pool_id=pool.id, wallet_address=checkin_data.wallet_address)
    if participant is None:
        raise PoolCheckinError("Participant not found in pool.")

    check_in_date = checkin_data.check_in_date or date.today()
    checkin = PoolCheckin(
        pool_id=pool.id,
        participant_id=participant.id,
        check_in_date=check_in_date,
        tx_hash=checkin_data.tx_hash,
    )
    db.add(checkin)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        error_text = str(error.orig).lower()
        if "uq_participant_checkin" in error_text or "pool_checkins.participant_id, pool_checkins.check_in_date" in error_text:
            raise PoolCheckinError("A check-in already exists for this participant on that date.") from error
        raise

    db.refresh(checkin)

    checkin_dates = [item.check_in_date for item in get_checkins_for_wallet(db, pool_id=pool.id, wallet_address=participant.wallet_address)]
    participant.days_completed = len(set(checkin_dates))
    participant.current_streak = _calculate_current_streak(checkin_dates, check_in_date)
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return checkin
