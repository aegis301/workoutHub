from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


# This linking model is needed for many-to-many relationship between Exercise and MuscleGroup.
class ExerciseMuscleGroupLink(SQLModel, table=True):
    exercise_id: Optional[int] = Field(default=None, foreign_key="exercise.id", primary_key=True)
    muscle_group_id: Optional[int] = Field(default=None, foreign_key="musclegroup.id", primary_key=True)


class ExerciseEquipmentLink(SQLModel, table=True):
    exercise_id: Optional[int] = Field(default=None, foreign_key="exercise.id", primary_key=True)
    equipment_id: Optional[int] = Field(default=None, foreign_key="equipment.id", primary_key=True)


class Equipment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)

    # SQLModel handles relationships natively with `Relationship`
    exercises: List["Exercise"] = Relationship(back_populates="equipment", link_model=ExerciseEquipmentLink)
    sets: List["Set"] = Relationship(back_populates="equipment")


class MuscleGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="musclegroup.id")

    # Self-referential relationship for parent-child muscle groups
    children: List["MuscleGroup"] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={"remote_side": "MuscleGroup.id"}  # SQLModel handles this automatically
    )
    parent: Optional["MuscleGroup"] = Relationship(back_populates="children")

    primary_exercises: List["Exercise"] = Relationship(back_populates="primary_muscle_group")
    secondary_exercises: List["Exercise"] = Relationship(back_populates="secondary_muscle_groups", link_model=ExerciseMuscleGroupLink)


class ExerciseType(str, Enum):
    STRENGTH = "strength"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"


class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: ExerciseType = Field(sa_column_kwargs={"default": ExerciseType.STRENGTH})
    primary_muscle_group_id: Optional[int] = Field(default=None, foreign_key="musclegroup.id")

    # Relationships to MuscleGroup and Equipment
    primary_muscle_group: Optional[MuscleGroup] = Relationship(back_populates="primary_exercises")
    secondary_muscle_groups: List["MuscleGroup"] = Relationship(back_populates="secondary_exercises", link_model=ExerciseMuscleGroupLink)
    equipment: List["Equipment"] = Relationship(back_populates="exercises", link_model=ExerciseEquipmentLink)
    sets: List["Set"] = Relationship(back_populates="exercise")


class Set(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    exercise_id: int = Field(foreign_key="exercise.id")
    equipment_id: Optional[int] = Field(default=None, foreign_key="equipment.id")
    date: datetime
    weight: Optional[float] = Field(default=None, ge=0.0)
    reps: Optional[int] = Field(default=None, ge=0)
    rpe: Optional[int] = Field(default=None, ge=1, le=10)  # Rate of Perceived Exertion
    notes: Optional[str] = Field(default=None, max_length=500)
    duration: Optional[int] = Field(default=None, ge=0)  # Duration in seconds for cardio exercises
    distance: Optional[float] = Field(default=None, ge=0.0)  # Distance in kilometers for cardio exercises

    # Relationship to Exercise
    exercise: Exercise = Relationship(back_populates="sets")
    equipment: Optional[Equipment] = Relationship(back_populates="sets")
