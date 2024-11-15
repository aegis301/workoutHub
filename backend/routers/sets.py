import msgpack
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlmodel import Session, select
from typing import List
from ..models.models import Set, MuscleGroup, Exercise
from ..database import get_session
from ..logger.logger import Logger
from .utils import enrich_sets
router = APIRouter(
    prefix="/sets",
    tags=["sets"],
)

logger = Logger(__name__)


# Utility function to recursively get all children muscle groups
def get_all_muscle_group_ids(muscle_group_id: int, session: Session) -> List[int]:
    ids = [muscle_group_id]
    statement = select(MuscleGroup).where(MuscleGroup.parent_id == muscle_group_id)
    child_groups = session.exec(statement).all()

    for group in child_groups:
        ids.extend(get_all_muscle_group_ids(group.id, session))

    return ids


@router.get("/")
async def get_sets(db: Session = Depends(get_session)):
    statement = select(Set)
    sets = db.exec(statement).all()

    sets_dict = enrich_sets(sets)

    packed_sets = msgpack.packb(sets_dict, use_bin_type=True)
    return Response(content=packed_sets, media_type="application/msgpack")


@router.get("/{set_id}")
async def get_set(set_id: int, db: Session = Depends(get_session)):
    set = db.get(Set, set_id)
    if set is None:
        raise HTTPException(status_code=404, detail="Set not found")

    # Convert Set object to dictionary
    set_dict = set.model_dump()

    packed_set = msgpack.packb(set_dict, use_bin_type=True)
    return Response(content=packed_set, media_type="application/msgpack")


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

    # Convert Set objects to dictionaries
    results_dict = [result.model_dump() for result in results]

    packed_results = msgpack.packb(results_dict, use_bin_type=True)
    return Response(content=packed_results, media_type="application/msgpack")


# get sets by a certain time window
@router.get("/time_window/{start_date}/{end_date}", response_model=List[Set])
def get_sets_by_time_window(start_date: str, end_date: str, session: Session = Depends(get_session)):
    statement = select(Set).where(Set.date >= start_date, Set.date <= end_date)
    results = session.exec(statement).all()

    # Convert Set objects to dictionaries
    results_dict = [result.model_dump() for result in results]

    packed_results = msgpack.packb(results_dict, use_bin_type=True)
    return Response(content=packed_results, media_type="application/msgpack")


# get sets by a certain time windwow and muscle group
@router.get("/time_window/{start_date}/{end_date}/primary_muscle_group/{primary_muscle_group_name}", response_model=List[Set])
def get_sets_by_time_window_and_muscle_group(start_date: str, end_date: str, primary_muscle_group_name: str, session: Session = Depends(get_session)):
    # Get the muscle group by name
    group_statement = select(MuscleGroup).where(MuscleGroup.name == primary_muscle_group_name)
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
        .where(Set.date >= start_date, Set.date <= end_date, MuscleGroup.id.in_(muscle_group_ids))
    )

    results = session.exec(statement).all()

    # Convert Set objects to dictionaries
    results_dict = [result.model_dump() for result in results]

    packed_results = msgpack.packb(results_dict, use_bin_type=True)
    return Response(content=packed_results, media_type="application/msgpack")


@router.get("/exercises/{exercise_id}", response_model=List[Set])
def get_sets_by_exercise(exercise_id: int, session: Session = Depends(get_session)):
    statement = select(Set).where(Set.exercise_id == exercise_id)
    results = session.exec(statement).all()

    # Convert Set objects to dictionaries
    results_dict = [result.model_dump() for result in results]

    packed_results = msgpack.packb(results_dict, use_bin_type=True)
    return Response(content=packed_results, media_type="application/msgpack")


@router.get("/exercises/equipment/{exercise_id}/{equipment_id}", response_model=List[Set])
def get_sets_by_exercise_and_equipment(exercise_id: int, equipment_id: int, session: Session = Depends(get_session)):
    statement = select(Set).where(
        (Set.exercise_id == exercise_id) & (Set.equipment_id == equipment_id)
    )
    results = session.exec(statement).all()

    # Convert Set objects to dictionaries
    results_dict = [result.model_dump() for result in results]

    packed_results = msgpack.packb(results_dict, use_bin_type=True)
    return Response(content=packed_results, media_type="application/msgpack")
