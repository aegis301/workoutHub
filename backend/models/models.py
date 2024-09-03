"""This module contains the Pydantic models for the database tables."""
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Equipment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class MuscleGroup(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="musclegroup.id")
    children: List["MuscleGroup"] = Relationship(
        sa_relationship=relationship("MuscleGroup", back_populates="parent", remote_side="[MuscleGroup.id]")
    )
    parent: Optional["MuscleGroup"] = Relationship(
        sa_relationship=relationship("MuscleGroup", back_populates="children")
    )

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

# class ExerciseBase(SQLModel):
#     name: str
#     primary_muscle_group: str
#     secondary_muscle_groups: Optional[List[str]] = None
#     equipment: Optional[List[str]] = None
#     type: str


# class ExerciseCreate(ExerciseBase):
#     pass


# class Exercise(ExerciseBase):
#     id: int

#     class Config:
#         orm_mode = True


# class SetBase(SQLModel):
#     exercise: str
#     date: str
#     weight: float
#     # reps: int
#     rpe: int
#     notes: str
#     duration: int
#     distance: float


# class SetCreate(SetBase):
#     pass


# class Set(SetBase):
#     id: int

#     class Config:
#         orm_mode = True


# class MuscleGroupBase(SQLModel):
#     name: str
#     children: Optional[List["MuscleGroup"]] = None

#     class Config:
#         arbitrary_types_allowed = True


# class MuscleGroupCreate(MuscleGroupBase):
#     pass


# class MuscleGroup(MuscleGroupBase):
#     id: int

#     class Config:
#         orm_mode = True
