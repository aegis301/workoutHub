"""
Exercise management endpoints.

This module provides REST API endpoints for managing exercises in the workout database.
Each exercise has a name, type, and primary muscle group association.
"""

import msgpack
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select

from ..database import get_session
from ..models.models import Exercise

router = APIRouter(
    prefix="/exercises",
    tags=["exercises"],
    responses={
        404: {"description": "Exercise not found"},
        422: {"description": "Validation error"},
    },
)


@router.get(
    "/",
    summary="Get all exercises",
    description="Retrieve a complete list of all exercises in the database with their muscle group associations.",
    response_description="MessagePack-encoded list of exercise objects"
)
async def get_exercises(db: Session = Depends(get_session)) -> Response:
    """
    Retrieve all exercises from the database.
    
    This endpoint returns all exercises with their basic information including
    name, type (Strength/Cardio/Flexibility), and primary muscle group targeting.
    
    Args:
        db (Session): Database session dependency injected by FastAPI
        
    Returns:
        Response: MessagePack-encoded response containing a list of exercise objects
        
    Raises:
        500: Internal server error if database connection fails
        
    Example:
        >>> GET /exercises/
        >>> Content-Type: application/msgpack
        >>> [
        ...   {
        ...     "id": 1,
        ...     "name": "Bench Press",
        ...     "type": "Strength",
        ...     "primary_muscle_group_id": 18
        ...   },
        ...   ...
        ... ]
    """
    statement = select(Exercise)
    exercises = db.exec(statement).all()

    # Convert Exercise objects to dictionaries for serialization
    exercises_dict = [exercise.model_dump() for exercise in exercises]

    packed_exercises = msgpack.packb(exercises_dict, use_bin_type=True)
    return Response(content=packed_exercises, media_type="application/msgpack")


@router.get("/{exercise_id}", summary="Get exercise by ID", description="Retrieve a specific exercise by its ID.")
async def get_exercise(exercise_id: int, db: Session = Depends(get_session)) -> Response:
    """
    Get a specific exercise by ID.
    
    Args:
        exercise_id: The ID of the exercise to retrieve
        db: Database session dependency
        
    Returns:
        Response: MessagePack-encoded exercise object
        
    Raises:
        404: Exercise not found
        422: Invalid exercise ID format
    """
    exercise = db.get(Exercise, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # Convert Exercise object to dictionary
    exercise_dict = exercise.model_dump()

    packed_exercise = msgpack.packb(exercise_dict, use_bin_type=True)
    return Response(content=packed_exercise, media_type="application/msgpack")
