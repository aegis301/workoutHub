import msgpack
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlmodel import Session, select
from ..models.models import MuscleGroup
from ..database import get_session

router = APIRouter(
    prefix="/muscle-groups",
    tags=["muscle-groups"],
)


@router.get("/")
async def get_muscle_groups(db: Session = Depends(get_session)):
    statement = select(MuscleGroup)
    muscle_groups = db.exec(statement).all()

    # Convert MuscleGroup objects to dictionaries
    muscle_groups_dict = [muscle_group.model_dump() for muscle_group in muscle_groups]

    packed_muscle_groups = msgpack.packb(muscle_groups_dict, use_bin_type=True)
    return Response(content=packed_muscle_groups, media_type="application/msgpack")


@router.get("/{muscle_group_id}")
async def get_muscle_group(muscle_group_id: int, db: Session = Depends(get_session)):
    muscle_group = db.get(MuscleGroup, muscle_group_id)
    if muscle_group is None:
        raise HTTPException(status_code=404, detail="Muscle group not found")

    # Convert MuscleGroup object to dictionary
    muscle_group_dict = muscle_group.model_dump()

    packed_muscle_group = msgpack.packb(muscle_group_dict, use_bin_type=True)
    return Response(content=packed_muscle_group, media_type="application/msgpack")
