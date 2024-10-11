from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..models.models import Set
from ..database import get_session

router = APIRouter(
    prefix="/sets",
    tags=["sets"],
)


@router.get("/")
def get_sets(db: Session = Depends(get_session)):
    statement = select(Set)
    muscle_groups = db.exec(statement).all()
    return muscle_groups


@router.get("/{set_id}")
def get_set(set_id: int, db: Session = Depends(get_session)):
    set = db.get(Set, set_id)
    return set


@router.post("/")
def create_set(set: Set, db: Session = Depends(get_session)):
    db.add(set)
    db.commit()
    db.refresh(set)
    return set


@router.get("/primary_muscle_group/{primary_muscle_group_name}")
def get_set_by_primary_muscle_group_name(primary_muscle_group_name: str, db: Session = Depends(get_session)):
    statement = select(Set).where(Set.exercise.primary_muscle_group == primary_muscle_group_name)
    sets = db.exec(statement).all()
    return sets
