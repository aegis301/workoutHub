"""This module contains the Pydantic models for the database tables."""
from typing import List, Optional
from sqlmodel import Field, SQLModel


class ExerciseBase(SQLModel):
    name: str
    primary_muscle_group: str
    secondary_muscle_groups: Optional[List[str]] = None
    equipment: Optional[List[str]] = None
    type: str


class ExerciseCreate(ExerciseBase):
    pass


class Exercise(ExerciseBase):
    id: int

    class Config:
        orm_mode = True


class SetBase(SQLModel):
    exercise: str
    date: str
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


class MuscleGroupBase(SQLModel):
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
