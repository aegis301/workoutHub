"""
Set management endpoints.

This module provides REST API endpoints for managing workout sets,
which represent individual exercises performed with specific weight, reps, RPE, etc.
"""

from datetime import datetime
from typing import List

import msgpack
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select

from ..database import get_session
from ..logger.logger import Logger
from ..models.models import Exercise, MuscleGroup, Set
from .utils import enrich_sets

router = APIRouter(
    prefix="/sets",
    tags=["sets"],
    responses={
        404: {"description": "Set not found"},
        422: {"description": "Validation error"},
    },
)

logger = Logger(__name__)


def serialize_for_msgpack(obj_dict: dict) -> dict:
    """
    Convert datetime objects to ISO strings for MessagePack serialization.

    Args:
        obj_dict: Dictionary that may contain datetime objects

    Returns:
        dict: Dictionary with datetime objects converted to ISO strings
    """
    result = {}
    for key, value in obj_dict.items():
        if isinstance(value, datetime):
            result[key] = value.isoformat()
        else:
            result[key] = value
    return result


def get_all_muscle_group_ids(muscle_group_id: int, session: Session) -> List[int]:
    """
    Recursively get all children muscle group IDs for hierarchical queries.

    Args:
        muscle_group_id: The parent muscle group ID
        session: Database session

    Returns:
        List[int]: List of muscle group IDs including the parent and all children
    """
    ids = [muscle_group_id]
    statement = select(MuscleGroup).where(
        MuscleGroup.parent_id == muscle_group_id)
    child_groups = session.exec(statement).all()

    for group in child_groups:
        if group.id:  # Ensure the ID is not None
            ids.extend(get_all_muscle_group_ids(group.id, session))

    return ids


@router.get("/", summary="Get all sets", description="Retrieve all workout sets with enriched exercise and muscle group data.")
async def get_sets(db: Session = Depends(get_session)) -> Response:
    """
    Get all workout sets from the database.

    Returns all sets with enriched data including exercise names,
    muscle group information, and main muscle group categorization.

    Args:
        db: Database session dependency

    Returns:
        Response: MessagePack-encoded list of enriched set objects

    Raises:
        500: Database connection error
    """
    statement = select(Set)
    sets = db.exec(statement).all()

    # Convert to list to handle the enrich_sets function
    sets_list = list(sets)
    sets_dict = enrich_sets(sets_list)

    # The enrich_sets function now handles datetime serialization

    packed_sets = msgpack.packb(sets_dict, use_bin_type=True)
    return Response(content=packed_sets, media_type="application/msgpack")


@router.get("/{set_id}", summary="Get set by ID", description="Retrieve a specific workout set by its ID.")
async def get_set(set_id: int, db: Session = Depends(get_session)) -> Response:
    """
    Get a specific workout set by ID.

    Args:
        set_id: The ID of the set to retrieve
        db: Database session dependency

    Returns:
        Response: MessagePack-encoded set object

    Raises:
        404: Set not found
        422: Invalid set ID format
    """
    set = db.get(Set, set_id)
    if set is None:
        raise HTTPException(status_code=404, detail="Set not found")

    # Convert Set object to dictionary and handle datetime serialization
    set_dict = set.model_dump()
    serialized_set_dict = serialize_for_msgpack(set_dict)

    packed_set = msgpack.packb(serialized_set_dict, use_bin_type=True)
    return Response(content=packed_set, media_type="application/msgpack")


@router.get("/primary_muscle_group/{primary_muscle_group_name}", summary="Get sets by muscle group", description="Retrieve all sets for a muscle group and its children.")
def get_sets_by_muscle_group_and_children(muscle_group_name: str, session: Session = Depends(get_session)) -> Response:
    """
    Get all sets for a muscle group and its children.

    Args:
        muscle_group_name: The name of the muscle group
        session: Database session dependency

    Returns:
        Response: MessagePack-encoded list of sets for the muscle group

    Raises:
        404: Muscle group not found
        422: Invalid muscle group name format
    """
    # Get the muscle group by name
    group_statement = select(MuscleGroup).where(
        MuscleGroup.name == muscle_group_name)
    muscle_group = session.exec(group_statement).first()

    if not muscle_group or muscle_group.id is None:
        raise HTTPException(status_code=404, detail="Muscle group not found")

    # Get all muscle group IDs (including children)
    muscle_group_ids = get_all_muscle_group_ids(muscle_group.id, session)

    # Query sets by checking if exercise primary_muscle_group_id matches any of the target IDs
    # Use a simple OR condition for multiple muscle group IDs
    if len(muscle_group_ids) == 1:
        exercise_statement = select(Exercise.id).where(
            Exercise.primary_muscle_group_id == muscle_group_ids[0])
    else:
        # For multiple IDs, use OR conditions
        conditions = [Exercise.primary_muscle_group_id ==
                      mg_id for mg_id in muscle_group_ids]
        from sqlmodel import or_
        exercise_statement = select(Exercise.id).where(or_(*conditions))

    exercise_ids = [ex_id for ex_id in session.exec(exercise_statement).all()]

    # Then get sets for those exercises
    if len(exercise_ids) == 0:
        results = []
    elif len(exercise_ids) == 1:
        statement = select(Set).where(Set.exercise_id == exercise_ids[0])
        results = session.exec(statement).all()
    else:
        # For multiple IDs, use OR conditions
        conditions = [Set.exercise_id == ex_id for ex_id in exercise_ids]
        from sqlmodel import or_
        statement = select(Set).where(or_(*conditions))
        results = session.exec(statement).all()

    # Convert Set objects to dictionaries and handle datetime serialization
    results_dict = []
    for result in results:
        result_dict = result.model_dump()
        serialized_result = serialize_for_msgpack(result_dict)
        results_dict.append(serialized_result)

    packed_results = msgpack.packb(results_dict, use_bin_type=True)
    return Response(content=packed_results, media_type="application/msgpack")


# get sets by a certain time window
@router.get("/time_window/{start_date}/{end_date}", summary="Get sets by time window", description="Retrieve all sets within a specific date range.")
def get_sets_by_time_window(start_date: str, end_date: str, session: Session = Depends(get_session)) -> Response:
    """
    Get all sets within a specific time window.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        session: Database session dependency

    Returns:
        Response: MessagePack-encoded list of sets within the date range

    Raises:
        422: Invalid date format
    """
    try:
        # Parse string dates to datetime objects
        start_datetime = datetime.fromisoformat(start_date)
        end_datetime = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(
            status_code=422, detail="Invalid date format. Use YYYY-MM-DD format.")

    statement = select(Set).where(
        Set.date >= start_datetime, Set.date <= end_datetime)
    results = session.exec(statement).all()

    # Convert Set objects to dictionaries and handle datetime serialization
    results_dict = []
    for result in results:
        result_dict = result.model_dump()
        serialized_result = serialize_for_msgpack(result_dict)
        results_dict.append(serialized_result)

    packed_results = msgpack.packb(results_dict, use_bin_type=True)
    return Response(content=packed_results, media_type="application/msgpack")


# get sets by a certain time window and muscle group
@router.get("/time_window/{start_date}/{end_date}/primary_muscle_group/{primary_muscle_group_name}", summary="Get sets by time window and muscle group", description="Retrieve all sets within a date range for a specific muscle group and its children.")
def get_sets_by_time_window_and_muscle_group(start_date: str, end_date: str, primary_muscle_group_name: str, session: Session = Depends(get_session)) -> Response:
    """
    Get all sets within a time window for a specific muscle group and its children.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        primary_muscle_group_name: The name of the muscle group
        session: Database session dependency

    Returns:
        Response: MessagePack-encoded list of sets for the muscle group within the date range

    Raises:
        404: Muscle group not found
        422: Invalid date format or muscle group name
    """
    try:
        # Parse string dates to datetime objects
        start_datetime = datetime.fromisoformat(start_date)
        end_datetime = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(
            status_code=422, detail="Invalid date format. Use YYYY-MM-DD format.")

    # Get the muscle group by name
    group_statement = select(MuscleGroup).where(
        MuscleGroup.name == primary_muscle_group_name)
    muscle_group = session.exec(group_statement).first()

    if not muscle_group or muscle_group.id is None:
        raise HTTPException(status_code=404, detail="Muscle group not found")

    # Get all muscle group IDs (including children)
    muscle_group_ids = get_all_muscle_group_ids(muscle_group.id, session)

    # Query sets for the muscle group and all its children within the time window
    # Use a similar approach as above for muscle group filtering
    if len(muscle_group_ids) == 1:
        exercise_statement = select(Exercise.id).where(
            Exercise.primary_muscle_group_id == muscle_group_ids[0])
    else:
        # For multiple IDs, use OR conditions
        conditions = [Exercise.primary_muscle_group_id ==
                      mg_id for mg_id in muscle_group_ids]
        from sqlmodel import or_
        exercise_statement = select(Exercise.id).where(or_(*conditions))

    exercise_ids = [ex_id for ex_id in session.exec(exercise_statement).all()]

    # Then get sets for those exercises within the time window
    if len(exercise_ids) == 0:
        results = []
    elif len(exercise_ids) == 1:
        statement = select(Set).where(
            Set.date >= start_datetime,
            Set.date <= end_datetime,
            Set.exercise_id == exercise_ids[0]
        )
        results = session.exec(statement).all()
    else:
        # For multiple IDs, use OR conditions
        exercise_conditions = [Set.exercise_id ==
                               ex_id for ex_id in exercise_ids]
        from sqlmodel import or_
        statement = select(Set).where(
            Set.date >= start_datetime,
            Set.date <= end_datetime,
            or_(*exercise_conditions)
        )
        results = session.exec(statement).all()

    # Convert Set objects to dictionaries and handle datetime serialization
    results_dict = []
    for result in results:
        result_dict = result.model_dump()
        serialized_result = serialize_for_msgpack(result_dict)
        results_dict.append(serialized_result)

    packed_results = msgpack.packb(results_dict, use_bin_type=True)
    return Response(content=packed_results, media_type="application/msgpack")


@router.get("/exercises/{exercise_id}", summary="Get sets by exercise", description="Retrieve all sets for a specific exercise.")
def get_sets_by_exercise(exercise_id: int, session: Session = Depends(get_session)) -> Response:
    """
    Get all sets for a specific exercise.

    Args:
        exercise_id: The ID of the exercise to get sets for
        session: Database session dependency

    Returns:
        Response: MessagePack-encoded list of sets for the exercise

    Raises:
        422: Invalid exercise ID format
    """
    statement = select(Set).where(Set.exercise_id == exercise_id)
    results = session.exec(statement).all()

    # Convert Set objects to dictionaries and handle datetime serialization
    results_dict = []
    for result in results:
        result_dict = result.model_dump()
        serialized_result = serialize_for_msgpack(result_dict)
        results_dict.append(serialized_result)

    packed_results = msgpack.packb(results_dict, use_bin_type=True)
    return Response(content=packed_results, media_type="application/msgpack")


@router.get("/exercises/equipment/{exercise_id}/{equipment_id}", summary="Get sets by exercise and equipment", description="Retrieve all sets for a specific exercise using specific equipment.")
def get_sets_by_exercise_and_equipment(exercise_id: int, equipment_id: int, session: Session = Depends(get_session)) -> Response:
    """
    Get all sets for a specific exercise using specific equipment.

    Args:
        exercise_id: The ID of the exercise
        equipment_id: The ID of the equipment used
        session: Database session dependency

    Returns:
        Response: MessagePack-encoded list of sets for the exercise and equipment combination

    Raises:
        422: Invalid exercise ID or equipment ID format
    """
    statement = select(Set).where(
        (Set.exercise_id == exercise_id) & (Set.equipment_id == equipment_id)
    )
    results = session.exec(statement).all()

    # Convert Set objects to dictionaries and handle datetime serialization
    results_dict = []
    for result in results:
        result_dict = result.model_dump()
        serialized_result = serialize_for_msgpack(result_dict)
        results_dict.append(serialized_result)

    packed_results = msgpack.packb(results_dict, use_bin_type=True)
    return Response(content=packed_results, media_type="application/msgpack")
