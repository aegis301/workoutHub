import streamlit as st
import plotly.express as px
from utils import query_with_cache

# get the data from the server
sets = query_with_cache('http://localhost:8000/sets/')

st.title('workoutHub')

# Create a pie chart of sets by primary muscle group using Plotly
fig1 = px.pie(sets, names='primary_muscle_group_name', title='Sets by Primary Muscle Group')
# create a pie chart of sets by main muscle group using Plotly
fig2 = px.pie(sets, names='main_muscle_group', title='Sets by Main Muscle Group')


st.plotly_chart(fig1)
st.plotly_chart(fig2)

# Display the data
st.write(sets)
