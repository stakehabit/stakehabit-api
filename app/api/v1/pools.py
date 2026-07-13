from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.schemas.pool import (
    PoolCheckinCreate,
    PoolCreate,
    PoolParticipantBase,
    PoolParticipantRead,
    PoolRead,
    PoolCheckinRead,
)
from app.services.pool_service import (
    PoolCheckinError,
    PoolJoinError,
    create_pool,
    get_checkins_for_wallet,
    get_pool_by_id,
    get_pool_participants,
    get_pools,
    join_pool,
    submit_checkin,
)

router = APIRouter()


@router.get("/pools", response_model=list[PoolRead])
def list_pools(db: Session = Depends(get_db)) -> list[PoolRead]:
    return get_pools(db)


@router.post("/pools", response_model=PoolRead, status_code=status.HTTP_201_CREATED)
def create_new_pool(pool_create: PoolCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)) -> PoolRead:
    pool = create_pool(db, pool_create=pool_create, creator_id=current_user.id)
    return pool


@router.get("/pools/{pool_id}", response_model=PoolRead)
def get_pool(pool_id: int, db: Session = Depends(get_db)) -> PoolRead:
    pool = get_pool_by_id(db, pool_id=pool_id)
    if pool is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pool not found")
    return pool


@router.post("/pools/{pool_id}/join", response_model=PoolParticipantRead)
def join_pool_endpoint(pool_id: int, participant: PoolParticipantBase, db: Session = Depends(get_db)) -> PoolParticipantRead:
    pool = get_pool_by_id(db, pool_id=pool_id)
    if pool is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pool not found")
    try:
        return join_pool(db, pool=pool, participant_data=participant)
    except PoolJoinError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.get("/pools/{pool_id}/participants", response_model=list[PoolParticipantRead])
def list_participants(pool_id: int, db: Session = Depends(get_db)) -> list[PoolParticipantRead]:
    pool = get_pool_by_id(db, pool_id=pool_id)
    if pool is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pool not found")
    return get_pool_participants(db, pool_id=pool_id)


@router.post("/pools/{pool_id}/checkin", response_model=PoolCheckinRead, status_code=status.HTTP_201_CREATED)
def create_pool_checkin(pool_id: int, checkin: PoolCheckinCreate, db: Session = Depends(get_db)) -> PoolCheckinRead:
    pool = get_pool_by_id(db, pool_id=pool_id)
    if pool is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pool not found")
    try:
        return submit_checkin(db, pool=pool, checkin_data=checkin)
    except PoolCheckinError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.get("/pools/{pool_id}/checkins/{wallet_address}", response_model=list[PoolCheckinRead])
def get_pool_checkins(pool_id: int, wallet_address: str, db: Session = Depends(get_db)) -> list[PoolCheckinRead]:
    pool = get_pool_by_id(db, pool_id=pool_id)
    if pool is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pool not found")
    return get_checkins_for_wallet(db, pool_id=pool_id, wallet_address=wallet_address)
