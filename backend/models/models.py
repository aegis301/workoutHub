from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum


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
    type: str
    primary_muscle_group_id: Optional[int] = Field(default=None, foreign_key="musclegroup.id")

    # Relationships to MuscleGroup and Equipment
    primary_muscle_group: MuscleGroup = Relationship(back_populates="primary_exercises")
    secondary_muscle_groups: List["MuscleGroup"] = Relationship(back_populates="secondary_exercises", link_model=ExerciseMuscleGroupLink)
    equipment: List["Equipment"] = Relationship(back_populates="exercises", link_model=ExerciseEquipmentLink)
    sets: List["Set"] = Relationship(back_populates="exercise")


class Set(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    exercise_id: int = Field(foreign_key="exercise.id")
    equipment_id: Optional[int] = Field(default=None, foreign_key="equipment.id")
    date: str
    weight: Optional[float]
    reps: Optional[int]
    rpe: Optional[int]
    notes: Optional[str]
    duration: Optional[int]
    distance: Optional[float]

    # Relationship to Exercise
    exercise: Exercise = Relationship(back_populates="sets")
    equipment: Equipment = Relationship(back_populates="sets")
