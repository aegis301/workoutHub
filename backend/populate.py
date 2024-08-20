"""Used to populate the database with dummy data for testing purposes."""
from sqlalchemy.orm import Session

from models import models, schemas

import json
import os


def create_muscle_groupsfvfg(db: Session):
    pass
    # # Create muscle groups
    # with open(os.path.join(os.path.dirname(__file__), 'muscle_groups.json')) as f:
    #     muscle_groups = json.load(f)
    # for muscle_group in muscle_groups:
    #     db_muscle_group = models.MuscleGroup(
    #         name=muscle_group['name']
    #     )
    #     db.add(db_muscle_group)
    # db.commit()


def create_exercises(db: Session):
    # Create exercises
    with open(os.path.join(os.path.dirname(__file__), 'exercises.json')) as f:
        exercises = json.load(f)
    for exercise in exercises:
        primary_muscle_group_db = db.query(models.MuscleGroup).filter(
            models.MuscleGroup.name == exercise['primary_muscle_group']).first()
        secondary_muscle_groups_db = []
        if exercise['secondary_muscle_groups']:
            for secondary_muscle_group in exercise['secondary_muscle_groups']:
                secondary_muscle_group_db = db.query(models.MuscleGroup).filter(
                    models.MuscleGroup.name == secondary_muscle_group).first()
                secondary_muscle_groups_db.append(secondary_muscle_group_db)

        db_exercise = models.Exercise(
            name=exercise['name'],
            type=exercise['type'],
            primary_muscle_group=primary_muscle_group_db,
            secondary_muscle_groups=secondary_muscle_groups_db,
        )
        db.add(db_exercise)
    db.commit()

    # Create sets
    with open(os.path.join(os.path.dirname(__file__), 'sets.json')) as f:
        sets = json.load(f)
    for set in sets:
        exercise_db = db.query(models.Exercise).filter(
            models.Exercise.name == set['exercise']).first()
        db_set = models.Set(
            exercise=exercise_db,
            weight=set['weight'],
            reps=set['reps'],
            rpe=set['rpe'],
            notes=set['notes'],
            duration=set['duration'],
            distance=set['distance']
        )
        db.add(db_set)
    db.commit()
