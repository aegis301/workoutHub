import msgpack
from fastapi import APIRouter, Depends, Response
from sqlmodel import Session, select
from ..models.models import Equipment
from ..database import get_session

router = APIRouter(
    prefix="/equipment",
    tags=["equipment"],
)


@router.get("/")
async def get_all_equipment(db: Session = Depends(get_session)):
    statement = select(Equipment)
    equipment = db.exec(statement).all()

    # Convert Equipment objects to dictionaries
    equipment_dict = [item.model_dump() for item in equipment]

    packed_equipment = msgpack.packb(equipment_dict, use_bin_type=True)
    return Response(content=packed_equipment, media_type="application/msgpack")


@router.get("/{equipment_id}")
async def get_equipment(equipment_id: int, db: Session = Depends(get_session)):
    statement = select(Equipment).where(Equipment.id == equipment_id)
    equipment = db.exec(statement).first()

    if equipment is None:
        return Response(status_code=404, content="Equipment not found")

    # Convert Equipment object to dictionary
    equipment_dict = equipment.model_dump()

    packed_equipment = msgpack.packb(equipment_dict, use_bin_type=True)
    return Response(content=packed_equipment, media_type="application/msgpack")
