from typing import List
from ..models.models import Set


def enrich_sets(sets: List[Set]) -> List[dict]:
    # Convert Set objects to dictionaries with additional fields
    sets_dict = []
    for set in sets:
        set_dict = set.model_dump()
        set_dict['exercise_name'] = set.exercise.name
        set_dict['primary_muscle_group_name'] = set.exercise.primary_muscle_group.name
        sets_dict.append(set_dict)

    return sets_dict
