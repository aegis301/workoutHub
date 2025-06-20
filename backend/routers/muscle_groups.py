"""
Muscle group management endpoints.

This module provides REST API endpoints for managing muscle groups
in a hierarchical structure, supporting parent-child relationships.
"""

import msgpack
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select

from ..database import get_session
from ..models.models import MuscleGroup

router = APIRouter(
    prefix="/muscle-groups",
    tags=["muscle-groups"],
    responses={
        404: {"description": "Muscle group not found"},
        422: {"description": "Validation error"},
    },
)


@router.get("/", summary="Get all muscle groups", description="Retrieve a list of all muscle groups with hierarchical relationships.")
async def get_muscle_groups(db: Session = Depends(get_session)) -> Response:
    """
    Get all muscle groups in the database.
    
    Returns a list of all muscle groups including their hierarchical relationships.
    Muscle groups can have parent-child relationships for organization
    (e.g., Upper Body -> Chest -> Upper Chest).
    
    Args:
        db: Database session dependency
        
    Returns:
        Response: MessagePack-encoded list of muscle group objects
        
    Raises:
        500: Database connection error
    """
    statement = select(MuscleGroup)
    muscle_groups = db.exec(statement).all()

    # Convert MuscleGroup objects to dictionaries
    muscle_groups_dict = [muscle_group.model_dump() for muscle_group in muscle_groups]

    packed_muscle_groups = msgpack.packb(muscle_groups_dict, use_bin_type=True)
    return Response(content=packed_muscle_groups, media_type="application/msgpack")


@router.get("/{muscle_group_id}", summary="Get muscle group by ID", description="Retrieve a specific muscle group by its ID.")
async def get_muscle_group(muscle_group_id: int, db: Session = Depends(get_session)) -> Response:
    """
    Get a specific muscle group by ID.
    
    Args:
        muscle_group_id: The ID of the muscle group to retrieve
        db: Database session dependency
        
    Returns:
        Response: MessagePack-encoded muscle group object
        
    Raises:
        404: Muscle group not found
        422: Invalid muscle group ID format
    """
    muscle_group = db.get(MuscleGroup, muscle_group_id)
    if muscle_group is None:
        raise HTTPException(status_code=404, detail="Muscle group not found")

    # Convert MuscleGroup object to dictionary
    muscle_group_dict = muscle_group.model_dump()

    packed_muscle_group = msgpack.packb(muscle_group_dict, use_bin_type=True)
    return Response(content=packed_muscle_group, media_type="application/msgpack")