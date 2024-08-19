from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..database import Base

# Association table for the many-to-many relationship
exercise_secondary_muscle_group_association = Table(
    'exercise_secondary_muscle_group', Base.metadata,
    Column('exercise_id', Integer, ForeignKey('exercises.id')),
    Column('muscle_group_id', Integer, ForeignKey('muscle_groups.id'))
)


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String)
    primary_muscle_group_id = Column(Integer, ForeignKey('muscle_groups.id'))

    # Define the relationship to the primary MuscleGroup class
    primary_muscle_group = relationship(
        "MuscleGroup", foreign_keys=[primary_muscle_group_id])

    # Define the relationship to the secondary MuscleGroup class
    secondary_muscle_groups = relationship(
        "MuscleGroup",
        secondary=exercise_secondary_muscle_group_association,
        back_populates="exercises"
    )
    sets = relationship("Set", back_populates="exercise")


class MuscleGroup(Base):
    __tablename__ = "muscle_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    parent_id = Column(Integer, ForeignKey("muscle_groups.id"))

    # Define the relationship to the Exercise class
    exercises = relationship(
        "Exercise",
        secondary=exercise_secondary_muscle_group_association,
        back_populates="secondary_muscle_groups"
    )


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class Set(Base):
    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    weight = Column(Integer)
    reps = Column(Integer)
    rpe = Column(Integer)
    notes = Column(String)
    duration = Column(Integer)
    distance = Column(Integer)
    equipment = Column(Integer, ForeignKey('equipment.id'))
    exercies = relationship("Exercise", back_populates="sets")
