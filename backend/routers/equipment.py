from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..models.models import Equipment
from ..database import get_session

router = APIRouter(
    prefix="/equipment",
    tags=["equipment"],
)


@router.get("/")
def get_all_equipment(db: Session = Depends(get_session)):
    statement = select(Equipment)
    equipment = db.exec(statement).all()
    return equipment


@router.post("/")
def create_equipment(equipment: Equipment, db: Session = Depends(get_session)):
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment


@router.get("/{equipment_id}")
def get_equipment(equipment_id: int, db: Session = Depends(get_session)):
    statement = select(Equipment).where(Equipment.id == equipment_id)
    equipment = db.exec(statement).first()
    return equipment
