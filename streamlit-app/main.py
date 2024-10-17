import msgpack
import streamlit as st
import pandas as pd
import requests
import plotly.express as px


def convert_response_data_to_df(response_data):
    response_json = msgpack.unpackb(response_data.content, raw=False)
    return pd.DataFrame(response_json)


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

# Create a pie chart of sets by primary muscle group using Plotly
fig = px.pie(sets, names='name_y', title='Sets by Primary Muscle Group')
st.plotly_chart(fig)