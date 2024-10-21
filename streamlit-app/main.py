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

sets = convert_response_data_to_df(sets_response)

st.title('workoutHub')

# Display the data
st.write(sets)

# Create a pie chart of sets by primary muscle group using Plotly
fig = px.pie(sets, names='primary_muscle_group_name', title='Sets by Primary Muscle Group')
st.plotly_chart(fig)
