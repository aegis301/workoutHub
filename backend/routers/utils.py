from typing import List
from ..models.models import Set

MAIN_MUSCLE_GROUPS = {
    "Back": ["Back", "Latissimus", "Trapezius", "Rhomboids", "Erector Spinae"],
    "Chest": ["Chest", "Pectoralis Major", "Pectoralis Minor"],
    "Legs": ["Legs", "Quadriceps", "Hamstrings", "Calves"],
    "Shoulders": ["Shoulders", "Deltoids", "Rear Deltoids", "Lateral Deltoids", "Side Deltoids", "Front Deltoids"],
    "Arms": ["Arms", "Biceps", "Triceps", "Forearms"],
    "Trunk": ["Trunk", "Abs", "Obliques"],
}


def enrich_sets(sets: List[Set]) -> List[dict]:
    # Convert Set objects to dictionaries with additional fields
    sets_dict = []
    for set in sets:
        set_dict = set.model_dump()
        set_dict['exercise_name'] = set.exercise.name
        set_dict['primary_muscle_group_name'] = set.exercise.primary_muscle_group.name
        set_dict['main_muscle_group'] = next((k for k, v in MAIN_MUSCLE_GROUPS.items() if set_dict['primary_muscle_group_name'] in v), None)
        sets_dict.append(set_dict)

    return sets_dict
