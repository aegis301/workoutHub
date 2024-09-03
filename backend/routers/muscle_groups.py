from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models.models import MuscleGroup
from database import get_session

router = APIRouter(
    prefix="/muscle_groups",
    tags=["muscle_groups"],
)


@router.get("/")
def get_muscle_groups(db: Session = Depends(get_session)):
    statement = select(MuscleGroup)
    muscle_groups = db.exec(statement).all()
    return muscle_groups


@router.get("/{muscle_group_id}")
def get_muscle_group(muscle_group_id: int, db: Session = Depends(get_session)):
    muscle_group = db.get(MuscleGroup, muscle_group_id)
    return muscle_group


@router.post("/")
def create_muscle_group(muscle_group: MuscleGroup, db: Session = Depends(get_session)):
    db.add(muscle_group)
    db.commit()
    db.refresh(muscle_group)
    return muscle_group
