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


# Utility function to recursively get all children muscle groups
def get_all_muscle_group_ids(muscle_group_id: int, session: Session) -> List[int]:
    # Base query to get the muscle group itself and its children
    group_statement = select(MuscleGroup).where(MuscleGroup.parent_id == muscle_group_id)
    child_groups = session.exec(group_statement).all()

    # Gather all child IDs recursively
    ids = [muscle_group_id]
    for group in child_groups:
        ids.extend(get_all_muscle_group_ids(group.id, session))

    return ids


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
def get_sets_by_muscle_group_and_children(muscle_group_name: str, session: Session = Depends(get_session)):
    # Get the muscle group by name
    group_statement = select(MuscleGroup).where(MuscleGroup.name == muscle_group_name)
    muscle_group = session.exec(group_statement).first()

    if not muscle_group:
        raise HTTPException(status_code=404, detail="Muscle group not found")

    # Get all muscle group IDs (including children)
    muscle_group_ids = get_all_muscle_group_ids(muscle_group.id, session)

    # Query sets for the muscle group and all its children
    statement = (
        select(Set)
        .join(Set.exercise)
        .join(Exercise.primary_muscle_group)
        .where(MuscleGroup.id.in_(muscle_group_ids))
    )

    results = session.exec(statement).all()

    if not results:
        raise HTTPException(status_code=404, detail="No sets found for the given muscle group and its children")

    return results
