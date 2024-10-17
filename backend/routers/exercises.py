import msgpack
from fastapi import APIRouter, Depends, Response
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

    # Convert Exercise objects to dictionaries
    exercises_dict = [exercise.model_dump() for exercise in exercises]

    packed_exercises = msgpack.packb(exercises_dict, use_bin_type=True)
    return Response(content=packed_exercises, media_type="application/msgpack")


@router.get("/{exercise_id}")
async def get_exercise(exercise_id: int, db: Session = Depends(get_session)):
    exercise = db.get(Exercise, exercise_id)
    if exercise is None:
        return Response(status_code=404, content="Exercise not found")

    # Convert Exercise object to dictionary
    exercise_dict = exercise.model_dump()

    packed_exercise = msgpack.packb(exercise_dict, use_bin_type=True)
    return Response(content=packed_exercise, media_type="application/msgpack")
