import streamlit as st
import requests
import plotly.express as px
from utils import convert_response_data_to_df

# get the data from the server
sets_response = requests.get('http://localhost:8000/sets/')

sets = convert_response_data_to_df(sets_response)

st.title('workoutHub')

# Display the data
st.write(sets)

# Create a pie chart of sets by primary muscle group using Plotly
fig1 = px.pie(sets, names='primary_muscle_group_name', title='Sets by Primary Muscle Group')
# create a pie chart of sets by main muscle group using Plotly
fig2 = px.pie(sets, names='main_muscle_group', title='Sets by Main Muscle Group')


st.plotly_chart(fig1)
st.plotly_chart(fig2)
