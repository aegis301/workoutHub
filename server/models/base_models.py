from pydantic import BaseModel
from typing import List, Optional


class BaseExercise(BaseModel):
    name: str
    primary_muscle_group: str
    secondary_muscle_group: Optional[List[str]]
    equipment: Optional[List[str]]
    type: str


class BaseSet(BaseModel):
    exercise: str
    weight: float
    reps: int
    rpe: int
    notes: str
    duration: int
    distance: float


class MuscleGroup(BaseModel):
    name: str
    children: Optional[List["MuscleGroup"]] = None

    class Config:
        arbitrary_types_allowed = True
