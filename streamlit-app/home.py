import plotly.express as px
import streamlit as st
from utils import query_with_cache

# get the data from the server
sets = query_with_cache('http://localhost:8000/sets/')

st.title('workoutHub')

# Debug: Show what we actually got
st.write("Data shape:", sets.shape)
st.write("Columns:", sets.columns.tolist() if not sets.empty else "No columns - DataFrame is empty")
st.write("First few rows:", sets.head() if not sets.empty else "No data")

# Only create charts if we have data and the required columns
if not sets.empty and 'primary_muscle_group_name' in sets.columns:
    # Create a pie chart of sets by primary muscle group using Plotly
    fig1 = px.pie(sets, names='primary_muscle_group_name', title='Sets by Primary Muscle Group')
    st.plotly_chart(fig1)
else:
    st.error("Cannot create Primary Muscle Group chart - missing 'primary_muscle_group_name' column")

if not sets.empty and 'main_muscle_group' in sets.columns:
    # create a pie chart of sets by main muscle group using Plotly
    fig2 = px.pie(sets, names='main_muscle_group', title='Sets by Main Muscle Group')
    st.plotly_chart(fig2)
else:
    st.error("Cannot create Main Muscle Group chart - missing 'main_muscle_group' column")

# Display the data
st.write("Raw data:")
st.write(sets)
