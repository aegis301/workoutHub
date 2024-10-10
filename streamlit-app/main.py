import streamlit as st
import pandas as pd
import requests


# get the data from the server
sets_response = requests.get('http://localhost:8000/sets/')
exercises_response = requests.get('http://localhost:8000/exercises/')
muscle_groups_response = requests.get('http://localhost:8000/muscle_groups/')
equipment_response = requests.get('http://localhost:8000/equipment/')
# convert to pandas dataframe
data = sets_response.json()
data = pd.DataFrame(data)

st.title('workoutHub')

# Display the data
st.write(data)