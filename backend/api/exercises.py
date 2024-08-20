from sqlalchemy.orm import Session

from ..models import models, schemas


def get_exercise(db: Session, exercise_id: int):
    return db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()


def get_exercises(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Exercise).offset(skip).limit(limit).all()


def create_exercise(db: Session, exercise: schemas.ExerciseCreate):
    primary_muscle_group_db = db.query(models.MuscleGroup).filter(
        models.MuscleGroup.name == exercise.primary_muscle_group).first()
    if exercise.secondary_muscle_group:
        for secondary_muscle_group in exercise.secondary_muscle_group:
            secondary_muscle_groups_db = db.query(models.MuscleGroup).filter(
                models.MuscleGroup.name == secondary_muscle_group).first()

    db_exercise = models.Exercise(
        name=exercise.name,
        type=exercise.type,
        primary_muscle_group=primary_muscle_group_db,
        secondary_muscle_groups=secondary_muscle_groups_db,
    )
    # add optional fields
    if exercise.secondary_muscle_group:
        db_exercise.secondary_muscle_groups = [
            db.query(models.MuscleGroup).filter(
                models.MuscleGroup.id == muscle_group_id).first()
            for muscle_group_id in exercise.secondary_muscle_group
        ]
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise
