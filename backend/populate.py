"""Used to populate the database with dummy data for testing purposes."""
import sys
import os

# Add the root directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from models.models import Equipment, MuscleGroup
from logger.logger import Logger
import json
import requests

logger = Logger(__name__)

SERVER_URL = "http://localhost:8000"


def create_equipment(db: Session):
    # Create equipment
    current_dir = os.getcwd()
    equipment_file_path = os.path.join(
        current_dir, 'data', 'equipment.json')
    with open(equipment_file_path) as f:
        equipment = json.load(f)
    for equipment_name in equipment:
        statement = select(Equipment).where(Equipment.name == equipment_name)
        existing_equipment = db.exec(statement).first()
        if existing_equipment:
            logger.debug(f"Equipment {equipment_name} already exists.")
            continue
        db_equipment = Equipment(name=equipment_name)
        try:
            requests.post(f"{SERVER_URL}/equipment/", json=db_equipment.model_dump())
            logger.info(f"Added equipment: {equipment_name}")
        except Exception as e:
            logger.error(f"Error adding equipment {equipment_name}: {e}")


def create_muscle_groups(db: Session):
    def add_muscle_group(name, parent_id=None):
        db_muscle_group = MuscleGroup(name=name, parent_id=parent_id)
        try:
            response = requests.post(
                f"{SERVER_URL}/muscle-groups/", json=db_muscle_group.model_dump())
            response.raise_for_status()
            logger.info(f"Added muscle group: {name}")
            return response.json().get('id')
        except Exception as e:
            logger.error(f"Error adding muscle group {name}: {e}")
            return None

    def process_muscle_groups(muscle_groups, parent_id=None):
        for name, subgroups in muscle_groups.items():
            muscle_group_id = add_muscle_group(name, parent_id)
            if subgroups and muscle_group_id:
                process_muscle_groups(subgroups, muscle_group_id)

    current_dir = os.getcwd()
    muscle_groups_file_path = os.path.join(
        current_dir, 'data', 'muscle-groups.json')
    with open(muscle_groups_file_path) as f:
        muscle_groups = json.load(f)

    # Process muscle groups
    process_muscle_groups(muscle_groups)

# def create_exercises(db: Session):
#     # Create exercises
#     current_dir = os.getcwd()
#     exercises_file_path = os.path.join(
#         current_dir, 'data', 'exercises.json')
#     with open(exercises_file_path) as f:
#         exercises = json.load(f)
#     for exercise_name, exercise_data in exercises.items():
#         exercise = db.query(models_depr.Exercise).filter(
#             models_depr.Exercise.name == exercise_data['name']).first()
#         if exercise:
#             logger.debug(f"Exercise {exercise_data['name']} already exists.")
#             continue
#         primary_muscle_group_db = db.query(models_depr.MuscleGroup).filter(
#             models_depr.MuscleGroup.name == exercise_data['primaryMuscleGroup']).first()
#         secondary_muscle_groups_db = []
#         if exercise_data.get('secondaryMuscleGroups'):
#             for secondary_muscle_group in exercise_data['secondaryMuscleGroups']:
#                 secondary_muscle_group_db = db.query(models_depr.MuscleGroup).filter(
#                     models_depr.MuscleGroup.name == secondary_muscle_group).first()
#                 if secondary_muscle_group_db:
#                     secondary_muscle_groups_db.append(
#                         secondary_muscle_group_db)
#                 else:
#                     logger.warning(
#                         f"Secondary muscle group {secondary_muscle_group} not found.")

#         db_exercise = models_depr.Exercise(
#             name=exercise_data['name'],
#             type=exercise_data['type'],
#             primary_muscle_group=primary_muscle_group_db,
#             secondary_muscle_groups=secondary_muscle_groups_db,
#         )
#         db.add(db_exercise)
#         db.commit()


# def build_set(row, db):
#     try:
#         exercise_db = db.query(models_depr.Exercise).filter(
#             models_depr.Exercise.name == row['exercise']).first()
#     except AttributeError:
#         logger.error(f"Exercise {row['exercise']} not found.")
#         return None
#     try:
#         equipment_db = db.query(models_depr.Equipment).filter(
#             models_depr.Equipment.name == row['equipment']).first()
#     except AttributeError:
#         logger.error(f"Equipment {row['Equipment']} not found.")
#         return None

#     datetime = pd.to_datetime(row["Date"])  # Convert to datetime

#     db_set = models_depr.Set(
#         exercise=exercise_db,
#         date=datetime,
#         weight=row['Weight'],
#         reps=row['Reps'],
#         duration=row['Seconds'],
#         distance=row['Distance'],
#         equipment=equipment_db
#     )
#     db.add(db_set)
#     db.commit()


# def create_sets(db: Session, data: pd.DataFrame = None):
#     # Create sets
#     logger.info("Adding sets...")
#     data.apply(lambda row: build_set(row, db), axis=1)
#     logger.info("Sets added.")


if __name__ == '__main__':
    from database import get_session

    with next(get_session()) as db:
        create_equipment(db)
        create_muscle_groups(db)
    # create_database(POSTGRES_DB)
    # create_muscle_groups(db)
    # create_exercises(db)

    # apply converter
    # strong_csv.converter(apply_filter=False)
    # data = pd.read_csv(
    #     f'data/strong-{pd.Timestamp.today().strftime('%Y-%m-%d')}.csv')
    # create_sets(db, data)
    db.close()
