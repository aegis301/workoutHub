from pydantic import BaseModel
from typing import List, Optional


class BaseExercise(BaseModel):
    name: str
    primary_muscle_group: str
    secondary_muscle_group: Optional[List[str]] | None = None
    equipment: Optional[List[str]] | None = None
    type: str


class BaseSet(BaseModel):
    exercise: str
    weight: float | None = None
    reps: int | None = None
    rpe: int | None = None
    notes: str | None = None
    duration: int | None = None
    distance: float | None = None


class BaseEquipment(BaseModel):
    name: str


class MuscleGroup(BaseModel):
    name: str
    children: Optional[List["MuscleGroup"]] | None = None

    class Config:
        arbitrary_types_allowed = True
