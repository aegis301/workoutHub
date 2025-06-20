"""
Equipment management endpoints.

This module provides REST API endpoints for managing gym equipment
used in workout exercises.
"""

import msgpack
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select

from ..database import get_session
from ..models.models import Equipment

router = APIRouter(
    prefix="/equipment",
    tags=["equipment"],
    responses={
        404: {"description": "Equipment not found"},
        422: {"description": "Validation error"},
    },
)


@router.get("/", summary="Get all equipment", description="Retrieve a list of all available gym equipment.")
async def get_all_equipment(db: Session = Depends(get_session)) -> Response:
    """
    Get all equipment available in the gym.
    
    Returns a list of all equipment that can be used for exercises,
    including barbells, dumbbells, machines, and bodyweight options.
    
    Args:
        db: Database session dependency
        
    Returns:
        Response: MessagePack-encoded list of equipment objects
        
    Raises:
        500: Database connection error
    """
    statement = select(Equipment)
    equipment = db.exec(statement).all()

    # Convert Equipment objects to dictionaries
    equipment_dict = [item.model_dump() for item in equipment]

    packed_equipment = msgpack.packb(equipment_dict, use_bin_type=True)
    return Response(content=packed_equipment, media_type="application/msgpack")


@router.get("/{equipment_id}", summary="Get equipment by ID", description="Retrieve a specific piece of equipment by its ID.")
async def get_equipment(equipment_id: int, db: Session = Depends(get_session)) -> Response:
    """
    Get a specific piece of equipment by ID.
    
    Args:
        equipment_id: The ID of the equipment to retrieve
        db: Database session dependency
        
    Returns:
        Response: MessagePack-encoded equipment object
        
    Raises:
        404: Equipment not found
        422: Invalid equipment ID format
    """
    statement = select(Equipment).where(Equipment.id == equipment_id)
    equipment = db.exec(statement).first()

    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")

    # Convert Equipment object to dictionary
    equipment_dict = equipment.model_dump()

    packed_equipment = msgpack.packb(equipment_dict, use_bin_type=True)
    return Response(content=packed_equipment, media_type="application/msgpack")
