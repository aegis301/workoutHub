import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt


def convert_response_data_to_df(response_data):
    data = response_data.json()
    df = pd.DataFrame(data)
    return df


# get the data from the server
sets_response = requests.get('http://localhost:8000/sets/')
exercises_response = requests.get('http://localhost:8000/exercises/')
muscle_groups_response = requests.get('http://localhost:8000/muscle-groups/')

sets = convert_response_data_to_df(sets_response)
exercises = convert_response_data_to_df(exercises_response)
muscle_groups = convert_response_data_to_df(muscle_groups_response)

st.title('workoutHub')

# Display the data
st.write(sets)
st.write(exercises)
st.write(muscle_groups)

sets = pd.merge(sets, exercises, left_on='exercise_id', right_on='id')
sets = pd.merge(sets, muscle_groups, left_on='primary_muscle_group_id', right_on='id')
st.write(sets)

# pie chart of sets by primary muscle group
st.write(sets['name_y'].value_counts().plot.pie())
plt.show()
