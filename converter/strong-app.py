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


def filter_imports(data):
    """Exclude exercises that are already imported in the database, based on the last import date found in import.json"""
    # get last import date
    last_import_date = json.load(open('data/import.json'))['last_import_date']
    # get all data rows that have been imported since the last import date
    data = data[data['Date'] > last_import_date]
    # write todays date to import.json
    json.dump({'last_import_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')},
              open('data/import.json', 'w'))
    return data


def converter(apply_filter=False):
    data = pd.read_csv('data/strong.csv')
    # import exercise json
    exercises = json.load(open('data/exercises.json'))
    if apply_filter is True:
        data = filter_imports(data)
    # split exercise name and equipment
    data['exercise'], data['equipment'] = zip(
        *data['Exercise Name'].map(strip_appendix))
    data.drop(columns=["Workout Name", "Duration"], inplace=True)
    # augment data with exercise data
    data = data.apply(augment_row, axis=1, exercises=exercises)
    # export data with date of today
    data.to_csv(
        f'data/strong{pd.Timestamp.today().strftime('%Y-%m-%d')}.csv', index=False)


if __name__ == '__main__':
    converter()
