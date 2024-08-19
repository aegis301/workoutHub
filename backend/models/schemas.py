from pydantic import BaseModel
from typing import List, Optional


class ExerciseBase(BaseModel):
    name: str
    primary_muscle_group: str
    secondary_muscle_group: Optional[List[str]]
    equipment: Optional[List[str]]
    type: str


class ExerciseCreate(ExerciseBase):
    pass


class Exercise(ExerciseBase):
    id: int

    class Config:
        orm_mode = True


class SetBase(BaseModel):
    exercise: str
    weight: float
    reps: int
    rpe: int
    notes: str
    duration: int
    distance: float


class SetCreate(SetBase):
    pass


class Set(SetBase):
    id: int

    class Config:
        orm_mode = True


class MuscleGroupBase(BaseModel):
    name: str
    children: Optional[List["MuscleGroup"]] = None

    class Config:
        arbitrary_types_allowed = True


class MuscleGroupCreate(MuscleGroupBase):
    pass


class MuscleGroup(MuscleGroupBase):
    id: int

    class Config:
        orm_mode = True
