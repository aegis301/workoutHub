from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..models.models import Exercise
from ..database import get_session

router = APIRouter(
    prefix="/exercises",
    tags=["exercises"],
)


@router.get("/")
async def get_exercises(db: Session = Depends(get_session)):
    statement = select(Exercise)
    exercises = db.exec(statement).all()
    return exercises


@router.get("/{exercise_id}")
async def get_exercise(exercise_id: int, db: Session = Depends(get_session)):
    exercise = db.get(Exercise, exercise_id)
    return exercise


@router.post("/")
async def create_exercise(exercise: Exercise, db: Session = Depends(get_session)):
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise
