from datetime import datetime
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
    """
    Enriches a list of Set objects with additional fields for serialization.
    Each Set object is converted to a dictionary with the following additional fields:
    - exercise_name: Name of the exercise associated with the set
    - primary_muscle_group_name: Name of the primary muscle group associated with the exercise
    - main_muscle_group: Main muscle group category based on the primary muscle group
    - date: ISO formatted date string if the date is a datetime object
    
    Args:
        sets (List[Set]): A list of Set objects to be enriched.
    Returns:
        List[dict]: A list of dictionaries representing the enriched Set objects.
    """
    # Convert Set objects to dictionaries with additional fields
    sets_dict = []
    for set in sets:
        set_dict = set.model_dump()
        
        # Handle datetime serialization
        if 'date' in set_dict and isinstance(set_dict['date'], datetime):
            set_dict['date'] = set_dict['date'].isoformat()
            
        set_dict['exercise_name'] = set.exercise.name
        if set.exercise.primary_muscle_group:
            set_dict['primary_muscle_group_name'] = set.exercise.primary_muscle_group.name
            set_dict['main_muscle_group'] = next((k for k, v in MAIN_MUSCLE_GROUPS.items() if set_dict['primary_muscle_group_name'] in v), None)
        else:
            set_dict['primary_muscle_group_name'] = None
            set_dict['main_muscle_group'] = None
            
        sets_dict.append(set_dict)

    return sets_dict
