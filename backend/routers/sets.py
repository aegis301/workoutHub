from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select
from ..models.models import Set, Exercise, MuscleGroup
from ..database import get_session
from ..logger.logger import Logger
router = APIRouter(
    prefix="/sets",
    tags=["sets"],
)

logger = Logger(__name__)


@router.get("/")
async def get_sets(db: Session = Depends(get_session)):
    statement = select(Set)
    muscle_groups = db.exec(statement).all()
    return muscle_groups


@router.get("/{set_id}")
async def get_set(set_id: int, db: Session = Depends(get_session)):
    set = db.get(Set, set_id)
    return set


@router.post("/")
async def create_set(set: Set, db: Session = Depends(get_session)):
    db.add(set)
    db.commit()
    db.refresh(set)
    return set


@router.get("/primary_muscle_group/{primary_muscle_group_name}", response_model=List[Set])
def get_sets_by_muscle_group_name(muscle_group_name: str, session: Session = Depends(get_session)):
    # Query to select sets filtered by the muscle group name
    statement = (
        select(Set)
        .join(Set.exercise)
        .join(Exercise.primary_muscle_group)
        .where(MuscleGroup.name == muscle_group_name)
    )

    results = session.exec(statement).all()

    if not results:
        raise HTTPException(status_code=404, detail="No sets found for the given muscle group name")

    return results
