"""Used to populate the database with dummy data for testing purposes."""
from sqlalchemy.orm import Session
from models import models
from logger.logger import Logger
import json
import os

logger = Logger(__name__)


def create_muscle_groups(db: Session):
    def add_muscle_group(name, parent_id=None):
        logger.info(f"Adding muscle group: {name}")
        existing_muscle_group = db.query(
            models.MuscleGroup).filter_by(name=name).first()
        if existing_muscle_group:
            logger.info(f"Muscle group {name} already exists with id {
                        existing_muscle_group.id}")
            return existing_muscle_group.id
        db_muscle_group = models.MuscleGroup(name=name, parent_id=parent_id)
        db.add(db_muscle_group)
        db.commit()
        return db_muscle_group.id

    def process_muscle_groups(muscle_groups, parent_id=None):
        for name, subgroups in muscle_groups.items():
            muscle_group_id = add_muscle_group(name, parent_id)
            if subgroups:
                process_muscle_groups(subgroups, muscle_group_id)

    current_dir = os.getcwd()
    muscle_roups_file_path = os.path.join(
        current_dir, 'data', 'muscle-groups.json')
    with open(muscle_roups_file_path) as f:
        muscle_groups = json.load(f)

    # Process muscle groups
    process_muscle_groups(muscle_groups)


def create_exercises(db: Session):
    # Create exercises
    current_dir = os.getcwd()
    exercises_file_path = os.path.join(
        current_dir, 'data', 'exercises.json')
    with open(exercises_file_path) as f:
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


def create_sets(db: Session):
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


if __name__ == '__main__':
    from database import SessionLocal, Base, engine
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # create_database(POSTGRES_DB)
    create_muscle_groups(db)
    create_exercises(db)
    create_sets(db)
    db.close()
