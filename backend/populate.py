"""Used to populate the database with dummy data for testing purposes."""
import json
import csv
import sqlalchemy
from sqlmodel import Session, select
from models.models import Equipment, MuscleGroup, Exercise, Set
from logger.logger import Logger
from pathlib import Path

logger = Logger(__name__)

# Determine the project root directory
project_root = Path(__file__).resolve().parent.parent


def create_equipment(db: Session):
    """Create equipment from a JSON file."""
    equipment_file_path = project_root / 'data' / 'equipment.json'
    with open(equipment_file_path) as f:
        equipment = json.load(f)

    for equipment_name in equipment:
        statement = select(Equipment).where(Equipment.name == equipment_name)
        existing_equipment = db.exec(statement).first()
        if existing_equipment:
            logger.debug(f"Equipment {equipment_name} already exists.")
            continue

        db_equipment = Equipment(name=equipment_name)
        db.add(db_equipment)
        db.commit()
        logger.info(f"Added equipment: {equipment_name}")


def create_muscle_groups(db: Session):
    """Create muscle groups from a nested JSON structure."""
    def add_muscle_group(name, parent_id=None):
        db_muscle_group = MuscleGroup(name=name, parent_id=parent_id)
        db.add(db_muscle_group)
        db.commit()
        logger.info(f"Added muscle group: {name}")
        return db_muscle_group.id

    def process_muscle_groups(muscle_groups, parent_id=None):
        for name, subgroups in muscle_groups.items():
            # Check if muscle group already exists
            statement = select(MuscleGroup).where(MuscleGroup.name == name)
            existing_muscle_group = db.exec(statement).first()
            if existing_muscle_group:
                logger.debug(f"Muscle group {name} already exists.")
                muscle_group_id = existing_muscle_group.id
            else:
                muscle_group_id = add_muscle_group(name, parent_id)
            if subgroups and muscle_group_id:
                process_muscle_groups(subgroups, muscle_group_id)

    muscle_groups_file_path = project_root / 'data' / 'muscle-groups.json'
    with open(muscle_groups_file_path) as f:
        muscle_groups = json.load(f)

    # Process muscle groups
    process_muscle_groups(muscle_groups)


def create_exercises(db: Session):
    """Create exercises from a JSON file."""
    exercises_file_path = project_root / 'data' / 'exercises.json'
    with open(exercises_file_path) as f:
        exercises = json.load(f)

    for exercise_name, exercise_data in exercises.items():
        statement = select(Exercise).where(Exercise.name == exercise_name)
        existing_exercise = db.exec(statement).first()
        if existing_exercise:
            logger.debug(f"Exercise {exercise_data['name']} already exists.")
            continue

        primary_muscle_group = db.exec(select(MuscleGroup).where(MuscleGroup.name == exercise_data['primaryMuscleGroup'])).first()
        secondary_muscle_groups = db.exec(select(MuscleGroup).where(MuscleGroup.name.in_(exercise_data['secondaryMuscleGroups']))).all()
        equipment_instances = db.exec(select(Equipment).where(Equipment.name.in_(exercise_data['equipment']))).all()

        if not isinstance(primary_muscle_group, MuscleGroup):
            logger.error(f"Primary muscle group not found for exercise: {exercise_data['name']}")
            continue
        if not secondary_muscle_groups:
            logger.error(f"Secondary muscle groups not found for exercise: {exercise_data['name']}")
        if not equipment_instances:
            logger.error(f"Equipment not found for exercise: {exercise_data['name']}")

        db_exercise = Exercise(
            name=exercise_data['name'],
            type=exercise_data['type'],
            primary_muscle_group=primary_muscle_group,
            secondary_muscle_groups=secondary_muscle_groups,
            equipment=equipment_instances
        )

        db.add(db_exercise)
        db.commit()
        logger.info(f"Added exercise: {exercise_data['name']}")


def create_sets(db: Session):
    """Create sets from a CSV file."""
    sets_file_path = project_root / 'data' / 'strong-2024-08-22.csv'
    with open(sets_file_path) as f:
        sets = csv.DictReader(f)

        for set_data in sets:
            statement = select(Exercise).where(Exercise.name == set_data['exercise'])
            exercise = db.exec(statement).first()

            statement = select(Equipment).where(Equipment.name == set_data['equipment'])
            equipment = db.exec(statement).first()

            db_set = Set(
                exercise=exercise,
                date=set_data['Date'],
                weight=float(set_data['Weight']),
                reps=int(set_data['Reps']),
                notes=set_data['Notes'],
                duration=int(set_data['Seconds']),
                distance=float(set_data['Distance']),
                equipment=equipment
            )

            db.add(db_set)
            try:
                db.commit()
            except sqlalchemy.exc.IntegrityError as e:
                logger.error(f"Failed to add set for exercise {set_data['exercise']}: {e}")
                db.rollback()
            logger.info(f"Added set for exercise {set_data['exercise']}")


def populate_db():
    from database import get_session

    with next(get_session()) as db:
        create_equipment(db)
        create_muscle_groups(db)
        create_exercises(db)
        create_sets(db)

    db.close()


if __name__ == '__main__':
    from database import get_session

    with next(get_session()) as db:
        create_equipment(db)
        create_muscle_groups(db)
        create_exercises(db)
        create_sets(db)

    db.close()