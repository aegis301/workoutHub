import pandas as pd
import json


def strip_appendix(s):
    """Strong exercise names contain an appendix with the equipment. This function splits the exercise from the appendix. E.g. 'Bench Press (Barbell)' -> 'Bench Press' and 'Barbell'"""
    return s.split(' (')[0], s.split(' (')[-1][:-1]


def augment_row(row, exercises):
    """Augment a row with the exercise data from the exercises.json file"""
    exercise = exercises[row['exercise']]
    row['primary_muscle_group'] = exercise['primaryMuscleGroup']
    row['secondary_muscle_group'] = exercise['secondaryMuscleGroups']
    return row


def main():
    data = pd.read_csv('data/strong.csv')
    # import exercise json
    exercises = json.load(open('data/exercises.json'))
    # split exercise name and equipment
    data['exercise'], data['equipment'] = zip(
        *data['Exercise Name'].map(strip_appendix))
    data.drop(columns=["Workout Name", "Duration"], inplace=True)
    # augment data with exercise data
    data = data.apply(augment_row, axis=1, exercises=exercises)
    # export data
    data.to_csv('data/strong_augmented.csv', index=False)


if __name__ == '__main__':
    main()
