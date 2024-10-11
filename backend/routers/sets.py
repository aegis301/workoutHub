from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..models.models import Set, MuscleGroup, Exercise
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


@router.get("/primary_muscle_group/{primary_muscle_group_name}")
async def get_set_by_primary_muscle_group_name(primary_muscle_group_name: str, db: Session = Depends(get_session)):
    # Fetch the MuscleGroup object by name
    muscle_group_statement = select(MuscleGroup).where(MuscleGroup.name == primary_muscle_group_name)
    muscle_group = db.exec(muscle_group_statement).first()

    if not muscle_group:
        raise HTTPException(status_code=404, detail="Muscle group not found")

    # Extract child muscle group ids
    for child in muscle_group.children:
        logger.debug(child)
    child_ids = [child.id for child in muscle_group.children]

    # Include the parent muscle group id
    muscle_group_ids = [muscle_group.id] + child_ids

    # Fetch all Set objects where the Exercise's primary_muscle_group_id matches one of the muscle group IDs
    sets_statement = select(Set).join(Set.exercise).where(Exercise.primary_muscle_group_id.in_(muscle_group_ids))
    sets = db.exec(sets_statement).all()

    return sets
