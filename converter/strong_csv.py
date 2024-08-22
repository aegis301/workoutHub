import os
import pandas as pd
import json
import datetime


def strip_appendix(s):
    """Strong exercise names contain an appendix with the equipment. This function splits the exercise from the appendix. E.g. 'Bench Press (Barbell)' -> 'Bench Press' and 'Barbell'"""
    return s.split(' (')[0], s.split(' (')[-1][:-1]


def augment_row(row, exercises):
    """Augment a row with the exercise data from the exercises.json file"""
    try:
        exercise = exercises[row['exercise']]
    except KeyError:
        print(f"Exercise {row['exercise']} not found.")
        return row
    row['primary_muscle_group'] = exercise['primaryMuscleGroup']
    row['secondary_muscle_group'] = exercise['secondaryMuscleGroups']
    return row


def filter_imports(data):
    """Exclude exercises that are already imported in the database, based on the last import date found in import.json"""
    # move all exports to the data/exports folder
    os.makedirs('data/exports', exist_ok=True)
    for file in os.listdir('data'):
        if file.startswith('strong-') and file.endswith('.csv'):
            os.rename(f'data/{file}', f'data/exports/{file}')
    # get the date of each old export
    dates = [pd.Timestamp(file.split('-', maxsplit=1)[-1].split('.')[0])
             for file in os.listdir('data/exports')]
    # convert dates to datetime
    dates = [datetime.datetime(date.year, date.month, date.day)
             for date in dates]
    # get the latest date
    latest_date = max(dates)
    # exclude sets that are already imported by comparing the dates
    data['Date'] = pd.to_datetime(data['Date'])
    data = data[data['Date'] > latest_date]
    return data


def converter(apply_filter=False):
    data = pd.read_csv('data/strong.csv')
    # import exercise json
    exercises = json.load(open('data/exercises.json'))
    if apply_filter is True:
        data = filter_imports(data)
    # split exercise name and equipment
    try:
        data['exercise'], data['equipment'] = zip(
            *data['Exercise Name'].map(strip_appendix))
    except ValueError:
        print(data['Exercise Name'].map(strip_appendix))
        data['exercise'] = data['Exercise Name']
    data.drop(columns=["Workout Name", "Duration"], inplace=True)
    # augment data with exercise data
    data = data.apply(augment_row, axis=1, exercises=exercises)
    # export data with date of today
    data.to_csv(
        f'data/strong-{pd.Timestamp.today().strftime('%Y-%m-%d')}.csv', index=False)


if __name__ == '__main__':
    converter()
